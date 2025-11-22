"""
Stripe payment integration and webhook handlers
"""
import stripe
import os
from decimal import Decimal
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import BillingSubscription, TrainerSubscription, Organization, Invoice, SubscriptionPlan
from .services import InvoiceService
import logging

logger = logging.getLogger(__name__)

# Initialize Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeService:
    """Service for Stripe payment integration"""
    
    @staticmethod
    def create_customer(user_or_org, email=None):
        """Create a Stripe customer"""
        if email is None:
            email = user_or_org.email if hasattr(user_or_org, 'email') else user_or_org.owner.email
        
        customer_metadata = {}
        customer_name = ""
        
        if isinstance(user_or_org, TrainerSubscription):
            customer_name = user_or_org.trainer.get_full_name()
            customer_metadata['trainer_id'] = str(user_or_org.trainer.id)
            customer_metadata['type'] = 'trainer'
        elif isinstance(user_or_org, Organization):
            customer_name = user_or_org.name
            customer_metadata['organization_id'] = str(user_or_org.id)
            customer_metadata['type'] = 'organization'
        
        try:
            customer = stripe.Customer.create(
                email=email,
                name=customer_name,
                metadata=customer_metadata,
                description=f"Customer for {customer_name}"
            )
            return customer.id
        except stripe.error.StripeError as e:
            logger.error(f"Stripe customer creation failed: {str(e)}")
            raise ValidationError(f"Payment provider error: {str(e)}")
    
    @staticmethod
    def create_subscription(user_or_org, plan, customer_id=None, trial_days=None):
        """Create a Stripe subscription"""
        if customer_id is None:
            customer_id = StripeService.create_customer(user_or_org)
        
        # Get or create Stripe product/price
        stripe_price_id = StripeService.get_or_create_price(plan)
        
        subscription_params = {
            'customer': customer_id,
            'items': [{'price': stripe_price_id}],
            'payment_behavior': 'default_incomplete',
            'expand': ['latest_invoice.payment_intent'],
            'metadata': {
                'plan_key': plan.key,
                'plan_id': str(plan.id),
            }
        }
        
        if trial_days:
            subscription_params['trial_period_days'] = trial_days
        
        try:
            subscription = stripe.Subscription.create(**subscription_params)
            return subscription
        except stripe.error.StripeError as e:
            logger.error(f"Stripe subscription creation failed: {str(e)}")
            raise ValidationError(f"Subscription creation failed: {str(e)}")
    
    @staticmethod
    def get_or_create_price(plan):
        """Get or create a Stripe price for a plan"""
        # In production, you'd store the Stripe price ID in the model
        # For now, create a product and price on demand
        product_id = f"prod_fitmo_{plan.key}"
        
        try:
            # Try to get existing product
            products = stripe.Product.list(limit=100)
            for product in products.data:
                if product.name == plan.name:
                    product_id = product.id
                    break
            else:
                # Create new product
                product = stripe.Product.create(
                    name=plan.name,
                    description=plan.description,
                    type='service',
                    metadata={'plan_key': plan.key}
                )
                product_id = product.id
            
            # Create price for this product
            price = stripe.Price.create(
                product=product_id,
                unit_amount=int(plan.price_monthly * 100),  # Convert to cents
                currency='mad',
                recurring={'interval': 'month', 'interval_count': 1},
                metadata={'plan_key': plan.key}
            )
            
            return price.id
        except stripe.error.StripeError as e:
            logger.error(f"Stripe price creation failed: {str(e)}")
            raise ValidationError(f"Price creation failed: {str(e)}")
    
    @staticmethod
    def cancel_subscription(stripe_subscription_id):
        """Cancel a Stripe subscription"""
        try:
            subscription = stripe.Subscription.delete(stripe_subscription_id)
            return subscription
        except stripe.error.StripeError as e:
            logger.error(f"Stripe subscription cancellation failed: {str(e)}")
            raise ValidationError(f"Cancellation failed: {str(e)}")
    
    @staticmethod
    def update_subscription(stripe_subscription_id, new_plan):
        """Update subscription to a new plan"""
        try:
            subscription = stripe.Subscription.retrieve(stripe_subscription_id)
            stripe_price_id = StripeService.get_or_create_price(new_plan)
            
            # Update the subscription
            updated_subscription = stripe.Subscription.modify(
                stripe_subscription_id,
                items=[{
                    'id': subscription['items']['data'][0].id,
                    'price': stripe_price_id,
                }],
                proration_behavior='create_prorations'
            )
            
            return updated_subscription
        except stripe.error.StripeError as e:
            logger.error(f"Stripe subscription update failed: {str(e)}")
            raise ValidationError(f"Update failed: {str(e)}")


def handle_subscription_updated(event):
    """Handle Stripe subscription.updated webhook"""
    subscription = event['data']['object']
    
    try:
        billing_sub = BillingSubscription.objects.get(
            provider_subscription_id=subscription['id']
        )
        
        # Update status based on Stripe subscription status
        status_map = {
            'active': 'active',
            'past_due': 'past_due',
            'cancelled': 'cancelled',
            'trialing': 'trial'
        }
        
        billing_sub.status = status_map.get(subscription['status'], 'active')
        billing_sub.current_period_end = timezone.datetime.fromtimestamp(
            subscription['current_period_end']
        )
        billing_sub.save()
        
        logger.info(f"Subscription {billing_sub.id} updated to {billing_sub.status}")
    except BillingSubscription.DoesNotExist:
        logger.warning(f"BillingSubscription not found for Stripe ID {subscription['id']}")


def handle_invoice_payment_failed(event):
    """Handle Stripe invoice.payment_failed webhook"""
    invoice = event['data']['object']
    
    try:
        billing_sub = BillingSubscription.objects.get(
            provider_subscription_id=invoice['subscription']
        )
        
        billing_sub.failed_payment_count += 1
        billing_sub.status = 'past_due'
        billing_sub.save()
        
        # Send email notification to user
        # TODO: Implement email notification
        
        logger.warning(f"Payment failed for subscription {billing_sub.id}")
    except BillingSubscription.DoesNotExist:
        logger.warning(f"BillingSubscription not found for invoice {invoice['id']}")


def handle_invoice_payment_succeeded(event):
    """Handle Stripe invoice.payment_succeeded webhook"""
    invoice = event['data']['object']
    
    try:
        billing_sub = BillingSubscription.objects.get(
            provider_subscription_id=invoice['subscription']
        )
        
        # Create invoice record
        if not invoice.get('paid'):
            return
        
        period_start = timezone.datetime.fromtimestamp(invoice['period_start']).date()
        period_end = timezone.datetime.fromtimestamp(invoice['period_end']).date()
        
        # Create or update invoice
        inv, created = Invoice.objects.get_or_create(
            provider_invoice_id=invoice['id'],
            defaults={
                'billing_subscription': billing_sub,
                'trainer_subscription': billing_sub.trainer_subscription,
                'organization': billing_sub.organization,
                'invoice_number': InvoiceService.generate_invoice_number(str(billing_sub.id)),
                'subtotal': Decimal(str(invoice['total'] / 100)),
                'tax_amount': Decimal(str(invoice['tax'] / 100) if invoice.get('tax') else 0),
                'total_amount': Decimal(str(invoice['total'] / 100)),
                'status': 'paid',
                'period_start': period_start,
                'period_end': period_end,
                'paid_date': timezone.now().date(),
                'due_date': period_end
            }
        )
        
        # Reset failed payment count
        billing_sub.failed_payment_count = 0
        billing_sub.status = 'active'
        billing_sub.save()
        
        logger.info(f"Payment succeeded for subscription {billing_sub.id}")
    except BillingSubscription.DoesNotExist:
        logger.warning(f"BillingSubscription not found for invoice {invoice['id']}")


def handle_customer_subscription_deleted(event):
    """Handle Stripe customer.subscription.deleted webhook"""
    subscription = event['data']['object']
    
    try:
        billing_sub = BillingSubscription.objects.get(
            provider_subscription_id=subscription['id']
        )
        
        billing_sub.status = 'cancelled'
        billing_sub.cancelled_at = timezone.now()
        billing_sub.save()
        
        logger.info(f"Subscription {billing_sub.id} cancelled via webhook")
    except BillingSubscription.DoesNotExist:
        logger.warning(f"BillingSubscription not found for Stripe ID {subscription['id']}")


@csrf_exempt
@require_http_methods(['POST'])
def stripe_webhook(request):
    """Handle Stripe webhooks"""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        logger.error("Invalid webhook payload")
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError:
        logger.error("Invalid webhook signature")
        return JsonResponse({'error': 'Invalid signature'}, status=400)
    
    # Handle different event types
    event_handlers = {
        'customer.subscription.updated': handle_subscription_updated,
        'invoice.payment_failed': handle_invoice_payment_failed,
        'invoice.payment_succeeded': handle_invoice_payment_succeeded,
        'customer.subscription.deleted': handle_customer_subscription_deleted,
    }
    
    handler = event_handlers.get(event['type'])
    if handler:
        try:
            handler(event)
        except Exception as e:
            logger.error(f"Error handling webhook {event['type']}: {str(e)}")
            return JsonResponse({'error': 'Webhook processing failed'}, status=500)
    
    return JsonResponse({'success': True}, status=200)
