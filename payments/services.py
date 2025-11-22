"""
Subscription and billing services
"""
from decimal import Decimal
from datetime import datetime, timedelta
from django.utils import timezone
from django.db import transaction
from django.core.exceptions import ValidationError
from .models import (
    SubscriptionPlan, Organization, TrainerSubscription, BillingSubscription, 
    OrganizationInvitation, SeatOverage, Invoice
)
from trainers.models import Trainer
from bookings.models import Booking
import uuid


class SubscriptionService:
    """Service for managing trainer subscriptions"""
    
    @staticmethod
    def create_trainer_subscription(user, plan_key, is_trial=True):
        """Create a new subscription for a trainer"""
        try:
            plan = SubscriptionPlan.objects.get(key=plan_key)
        except SubscriptionPlan.DoesNotExist:
            raise ValidationError(f"Plan {plan_key} does not exist")
        
        if TrainerSubscription.objects.filter(trainer=user).exists():
            raise ValidationError("Trainer already has a subscription")
        
        subscription = TrainerSubscription(
            trainer=user,
            plan=plan,
            is_trial=is_trial,
            trial_used=False
        )
        
        if is_trial and plan.is_trial_available:
            subscription.trial_start = timezone.now()
            subscription.trial_end = timezone.now() + timedelta(days=plan.trial_days)
        else:
            subscription.subscription_start = timezone.now()
            subscription.subscription_end = timezone.now() + timedelta(days=30)
        
        subscription.save()
        return subscription
    
    @staticmethod
    def upgrade_trainer_plan(user, new_plan_key):
        """Upgrade trainer to a different plan (handles proration)"""
        try:
            current_sub = TrainerSubscription.objects.get(trainer=user)
        except TrainerSubscription.DoesNotExist:
            raise ValidationError("Trainer has no active subscription")
        
        try:
            new_plan = SubscriptionPlan.objects.get(key=new_plan_key)
        except SubscriptionPlan.DoesNotExist:
            raise ValidationError(f"Plan {new_plan_key} does not exist")
        
        if current_sub.plan.id == new_plan.id:
            raise ValidationError("Already on this plan")
        
        # Update plan
        current_sub.plan = new_plan
        current_sub.updated_at = timezone.now()
        current_sub.save()
        
        return current_sub
    
    @staticmethod
    def calculate_prorated_price(current_plan, new_plan, days_remaining):
        """Calculate prorated price when upgrading mid-cycle"""
        if days_remaining <= 0:
            return new_plan.price_monthly
        
        daily_rate_current = current_plan.price_monthly / Decimal('30')
        daily_rate_new = new_plan.price_monthly / Decimal('30')
        
        credit = daily_rate_current * Decimal(str(days_remaining))
        new_charge = (daily_rate_new * Decimal(str(days_remaining + 30)))
        
        return max(Decimal('0'), new_charge - credit)
    
    @staticmethod
    def get_commission_rate(user):
        """Get commission rate for a trainer based on subscription"""
        try:
            sub = TrainerSubscription.objects.get(trainer=user)
            if sub.is_subscription_active and sub.plan:
                return sub.plan.commission_rate
        except TrainerSubscription.DoesNotExist:
            pass
        return Decimal('20')  # Default 20%


class OrganizationService:
    """Service for managing gym/organization accounts and subscriptions"""
    
    @staticmethod
    def create_organization(owner, name, email, plan_key=None):
        """Create a new organization (gym/club)"""
        if Organization.objects.filter(owner=owner).exists():
            raise ValidationError("User already owns an organization")
        
        organization = Organization(
            name=name,
            owner=owner,
            email=email
        )
        
        if plan_key:
            try:
                plan = SubscriptionPlan.objects.get(key=plan_key, is_org_plan=True)
                organization.subscription_plan = plan
                organization.is_trial = True
                organization.trial_start = timezone.now()
                organization.trial_end = timezone.now() + timedelta(days=plan.trial_days)
            except SubscriptionPlan.DoesNotExist:
                raise ValidationError(f"Organization plan {plan_key} does not exist")
        
        organization.save()
        return organization
    
    @staticmethod
    def can_add_trainer(organization):
        """Check if organization can add more trainers (seat availability)"""
        if not organization.subscription_plan:
            return False
        return organization.available_seats > 0
    
    @staticmethod
    def add_trainer_to_organization(organization, trainer_user):
        """Add a trainer to an organization"""
        if not OrganizationService.can_add_trainer(organization):
            raise ValidationError(
                f"Organization has no available seats. "
                f"Current: {organization.seats_used}/{organization.total_seats}"
            )
        
        # Check if trainer already linked to this org
        try:
            existing_sub = TrainerSubscription.objects.get(trainer=trainer_user)
            if existing_sub.organization == organization:
                raise ValidationError("Trainer already linked to this organization")
            if existing_sub.organization is not None:
                raise ValidationError("Trainer is already linked to another organization")
        except TrainerSubscription.DoesNotExist:
            pass
        
        # Create or update trainer subscription
        sub, created = TrainerSubscription.objects.get_or_create(trainer=trainer_user)
        sub.organization = organization
        sub.plan = organization.subscription_plan  # Inherit org plan
        sub.save()
        
        # Increment seats used
        organization.seats_used += 1
        organization.save()
        
        return sub
    
    @staticmethod
    def remove_trainer_from_organization(organization, trainer_user):
        """Remove a trainer from an organization"""
        try:
            sub = TrainerSubscription.objects.get(trainer=trainer_user, organization=organization)
            sub.organization = None
            sub.save()
            
            organization.seats_used = max(0, organization.seats_used - 1)
            organization.save()
            
            return True
        except TrainerSubscription.DoesNotExist:
            raise ValidationError("Trainer not found in this organization")
    
    @staticmethod
    def invite_trainer(organization, email, invited_by):
        """Create an invitation for a trainer to join organization"""
        # Check seat availability first
        if not OrganizationService.can_add_trainer(organization):
            raise ValidationError(
                f"No available seats. Current: {organization.seats_used}/{organization.total_seats}"
            )
        
        token = str(uuid.uuid4())
        expires_at = timezone.now() + timedelta(days=7)  # 7 day expiration
        
        invitation, created = OrganizationInvitation.objects.update_or_create(
            organization=organization,
            email=email,
            defaults={
                'token': token,
                'invited_by': invited_by,
                'accepted': False,
                'expires_at': expires_at
            }
        )
        
        return invitation
    
    @staticmethod
    def accept_invitation(token, trainer_user):
        """Accept an organization invitation"""
        try:
            invitation = OrganizationInvitation.objects.get(token=token)
        except OrganizationInvitation.DoesNotExist:
            raise ValidationError("Invalid invitation token")
        
        if not invitation.is_valid:
            raise ValidationError("This invitation has expired or was already accepted")
        
        if invitation.email.lower() != trainer_user.email.lower():
            raise ValidationError("This invitation is for a different email address")
        
        # Add trainer to organization
        OrganizationService.add_trainer_to_organization(invitation.organization, trainer_user)
        
        # Mark invitation as accepted
        invitation.accepted = True
        invitation.accepted_by = trainer_user
        invitation.accepted_at = timezone.now()
        invitation.save()
        
        return invitation
    
    @staticmethod
    def purchase_extra_seats(organization, num_seats):
        """Purchase additional trainer seats"""
        if num_seats <= 0:
            raise ValidationError("Must purchase at least 1 seat")
        
        if not organization.subscription_plan:
            raise ValidationError("Organization must have a subscription plan first")
        
        price_per_seat = organization.subscription_plan.overage_price_per_seat
        total_price = Decimal(str(num_seats)) * price_per_seat
        
        # Create seat overage record
        overage = SeatOverage(
            organization=organization,
            seats_purchased=num_seats,
            price_per_seat=price_per_seat,
            total_price=total_price,
            end_date=timezone.now().date() + timedelta(days=30)
        )
        overage.save()
        
        # Update organization
        organization.extra_seats_purchased += num_seats
        organization.save()
        
        return overage, total_price
    
    @staticmethod
    def upgrade_organization_plan(organization, new_plan_key):
        """Upgrade organization to a different plan"""
        if not organization.subscription_plan:
            raise ValidationError("Organization has no current plan")
        
        try:
            new_plan = SubscriptionPlan.objects.get(key=new_plan_key, is_org_plan=True)
        except SubscriptionPlan.DoesNotExist:
            raise ValidationError(f"Plan {new_plan_key} does not exist")
        
        if organization.subscription_plan.id == new_plan.id:
            raise ValidationError("Already on this plan")
        
        # Check if new plan has enough seats for current trainers
        if new_plan.included_seats < organization.seats_used:
            raise ValidationError(
                f"New plan only includes {new_plan.included_seats} seats, "
                f"but you have {organization.seats_used} trainers"
            )
        
        organization.subscription_plan = new_plan
        organization.extra_seats_purchased = 0  # Reset extra seats on upgrade
        organization.updated_at = timezone.now()
        organization.save()
        
        return organization


class CommissionService:
    """Service for calculating commissions and trainer earnings"""
    
    @staticmethod
    def calculate_booking_commission(booking):
        """Calculate commission for a booking based on trainer's plan"""
        trainer_user = booking.trainer.user
        commission_rate = SubscriptionService.get_commission_rate(trainer_user)
        
        # Calculate amounts
        booking.commission_rate = commission_rate
        booking.commission_amount = (booking.total_price * commission_rate) / Decimal('100')
        booking.trainer_earnings = booking.total_price - booking.commission_amount
        
        return booking
    
    @staticmethod
    def apply_booking_commission(booking):
        """Apply commission to booking and save"""
        CommissionService.calculate_booking_commission(booking)
        booking.save()
        return booking
    
    @staticmethod
    def get_trainer_earnings_summary(trainer_user, start_date=None, end_date=None):
        """Get earnings summary for a trainer"""
        bookings = Booking.objects.filter(trainer__user=trainer_user, status='completed')
        
        if start_date:
            bookings = bookings.filter(booking_date__gte=start_date)
        if end_date:
            bookings = bookings.filter(booking_date__lte=end_date)
        
        total_bookings = bookings.count()
        total_revenue = bookings.aggregate(
            total=models.Sum('total_price')
        )['total'] or Decimal('0')
        total_earnings = bookings.aggregate(
            total=models.Sum('trainer_earnings')
        )['total'] or Decimal('0')
        total_commission = bookings.aggregate(
            total=models.Sum('commission_amount')
        )['total'] or Decimal('0')
        
        return {
            'total_bookings': total_bookings,
            'total_revenue': total_revenue,
            'total_earnings': total_earnings,
            'total_commission': total_commission,
            'average_commission_rate': (total_commission / total_revenue * 100) if total_revenue > 0 else Decimal('0')
        }


class InvoiceService:
    """Service for managing invoices"""
    
    @staticmethod
    def generate_invoice_number(organization_or_trainer_id):
        """Generate unique invoice number"""
        now = timezone.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        return f"INV-{timestamp}-{organization_or_trainer_id[:8]}"
    
    @staticmethod
    def create_invoice(billing_subscription, period_start, period_end, amount):
        """Create an invoice for a subscription period"""
        invoice_number = InvoiceService.generate_invoice_number(str(billing_subscription.id))
        
        invoice = Invoice(
            billing_subscription=billing_subscription,
            trainer_subscription=billing_subscription.trainer_subscription,
            organization=billing_subscription.organization,
            invoice_number=invoice_number,
            subtotal=amount,
            tax_amount=Decimal('0'),  # Can be configured later
            total_amount=amount,
            period_start=period_start,
            period_end=period_end,
            due_date=timezone.now().date() + timedelta(days=30)
        )
        invoice.save()
        return invoice


# Import models at end to avoid circular imports
from django.db import models
