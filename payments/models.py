from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.utils import timezone
import uuid
from datetime import datetime, timedelta

User = get_user_model()


class PaymentGatewayConfig(models.Model):
    """Configuration for payment gateways"""
    GATEWAY_CHOICES = (
        ('stripe', 'Stripe'),
        ('paypal', 'PayPal'),
        ('cmi', 'CMI (Morocco)'),
    )
    
    gateway_name = models.CharField(max_length=50, choices=GATEWAY_CHOICES, unique=True)
    api_key = models.CharField(max_length=500)
    secret_key = models.CharField(max_length=500, blank=True)
    webhook_secret = models.CharField(max_length=500, blank=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'إعدادات بوابة الدفع'
        verbose_name_plural = 'إعدادات بوابات الدفع'
    
    def __str__(self):
        return f"{self.get_gateway_name_display()} - {'Active' if self.is_active else 'Inactive'}"


class SubscriptionPlan(models.Model):
    """Subscription plans for trainers and organizations (gyms/clubs)"""
    PLAN_TYPES = (
        ('basic', 'Basic'),
        ('premium', 'Premium'),
        ('club', 'Club'),
        ('gold_club', 'Gold Club'),
    )
    
    BILLING_PERIODS = (
        ('monthly', 'Monthly'),
        ('annual', 'Annual'),
    )
    
    key = models.CharField(max_length=50, unique=True, choices=PLAN_TYPES)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    # Pricing
    price_monthly = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    price_annual = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], null=True, blank=True)
    
    # Organization-specific (for gym plans)
    is_org_plan = models.BooleanField(default=False)  # True for Club/Gold Club
    included_seats = models.IntegerField(default=0)  # Number of trainer seats included
    overage_price_per_seat = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    
    # Features
    features = models.JSONField(default=list)  # List of feature strings
    booking_limit_per_month = models.IntegerField(null=True, blank=True)  # null = unlimited
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=20)  # Percentage (20 = 20%)
    
    # Trial
    trial_days = models.IntegerField(default=14)
    is_trial_available = models.BooleanField(default=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'خطة الاشتراك'
        verbose_name_plural = 'خطط الاشتراك'
        ordering = ['key']
    
    def __str__(self):
        return f"{self.name} ({self.price_monthly} MAD/month)"


class Organization(models.Model):
    """Gym/Club organization account"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_organizations')
    
    # Subscription info
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True, blank=True)
    subscription_start = models.DateTimeField(null=True, blank=True)
    subscription_end = models.DateTimeField(null=True, blank=True)
    is_trial = models.BooleanField(default=False)
    trial_start = models.DateTimeField(null=True, blank=True)
    trial_end = models.DateTimeField(null=True, blank=True)
    
    # Seat management
    seats_used = models.IntegerField(default=0)
    extra_seats_purchased = models.IntegerField(default=0)
    
    # Contact & Location
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    
    # Additional info
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='org_logos/', null=True, blank=True)
    website = models.URLField(blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'منظمة'
        verbose_name_plural = 'منظمات'
    
    def __str__(self):
        return self.name
    
    @property
    def available_seats(self):
        """Calculate available seats for this organization"""
        if not self.subscription_plan:
            return 0
        total_seats = self.subscription_plan.included_seats + self.extra_seats_purchased
        return total_seats - self.seats_used
    
    @property
    def total_seats(self):
        """Total seats including purchased extra"""
        if not self.subscription_plan:
            return 0
        return self.subscription_plan.included_seats + self.extra_seats_purchased
    
    @property
    def is_subscription_active(self):
        """Check if subscription is currently active (including trial)"""
        now = timezone.now()
        if self.is_trial and self.trial_end:
            return self.trial_end > now
        if self.subscription_end:
            return self.subscription_end > now
        return False


class TrainerSubscription(models.Model):
    """Individual trainer subscription"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    trainer = models.OneToOneField(User, on_delete=models.CASCADE, related_name='trainer_subscription')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    
    # Organization link (if trainer works for a gym)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True, 
                                    related_name='trainer_subscriptions')
    
    # Trial tracking
    is_trial = models.BooleanField(default=False)
    trial_start = models.DateTimeField(null=True, blank=True)
    trial_end = models.DateTimeField(null=True, blank=True)
    trial_used = models.BooleanField(default=False)  # Has trainer already used free trial?
    
    # Subscription period
    subscription_start = models.DateTimeField(null=True, blank=True)
    subscription_end = models.DateTimeField(null=True, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    auto_renew = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'اشتراك المدرب'
        verbose_name_plural = 'اشتراكات المدربين'
    
    def __str__(self):
        return f"{self.trainer.get_full_name()} - {self.plan.name if self.plan else 'No Plan'}"
    
    @property
    def is_subscription_active(self):
        """Check if subscription is currently active"""
        now = timezone.now()
        if self.is_trial and self.trial_end:
            return self.trial_end > now
        if self.subscription_end:
            return self.subscription_end > now
        return False
    
    @property
    def commission_rate(self):
        """Get commission rate for this trainer based on plan"""
        if self.plan:
            return self.plan.commission_rate
        return 20  # Default 20%


class BillingSubscription(models.Model):
    """Stripe/Payment provider subscription record"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Links to either trainer or organization
    trainer_subscription = models.OneToOneField(TrainerSubscription, on_delete=models.CASCADE, 
                                               null=True, blank=True, related_name='billing')
    organization = models.OneToOneField(Organization, on_delete=models.CASCADE, 
                                       null=True, blank=True, related_name='billing')
    
    # Payment provider info
    provider = models.CharField(max_length=50, default='stripe')  # stripe, paypal, cmi, etc.
    provider_subscription_id = models.CharField(max_length=200, blank=True)
    provider_customer_id = models.CharField(max_length=200, blank=True)
    
    # Subscription details
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    billing_period = models.CharField(max_length=20, choices=SubscriptionPlan.BILLING_PERIODS, default='monthly')
    
    # Status
    SUBSCRIPTION_STATUSES = (
        ('active', 'Active'),
        ('trial', 'Trial'),
        ('past_due', 'Past Due'),
        ('cancelled', 'Cancelled'),
        ('ended', 'Ended'),
    )
    status = models.CharField(max_length=20, choices=SUBSCRIPTION_STATUSES, default='trial')
    
    # Dates
    current_period_start = models.DateTimeField()
    current_period_end = models.DateTimeField()
    trial_start = models.DateTimeField(null=True, blank=True)
    trial_end = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    
    # Payment method
    payment_method_id = models.CharField(max_length=200, blank=True)
    
    # Tracking
    failed_payment_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'اشتراك الفواتير'
        verbose_name_plural = 'اشتراكات الفواتير'
    
    def __str__(self):
        if self.trainer_subscription:
            return f"Billing - {self.trainer_subscription.trainer.get_full_name()}"
        return f"Billing - {self.organization.name}"


class Invoice(models.Model):
    """Invoices for subscriptions"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Links
    billing_subscription = models.ForeignKey(BillingSubscription, on_delete=models.CASCADE, related_name='invoices')
    trainer_subscription = models.ForeignKey(TrainerSubscription, on_delete=models.SET_NULL, 
                                            null=True, blank=True, related_name='invoices')
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, 
                                    null=True, blank=True, related_name='invoices')
    
    # Invoice details
    invoice_number = models.CharField(max_length=50, unique=True)
    provider_invoice_id = models.CharField(max_length=200, blank=True)  # Stripe invoice ID etc
    
    # Amounts
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)  # Before VAT
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Status
    INVOICE_STATUSES = (
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('paid', 'Paid'),
        ('past_due', 'Past Due'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    )
    status = models.CharField(max_length=20, choices=INVOICE_STATUSES, default='draft')
    
    # Dates
    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    paid_date = models.DateField(null=True, blank=True)
    
    # Period covered
    period_start = models.DateField()
    period_end = models.DateField()
    
    # Notes
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'فاتورة'
        verbose_name_plural = 'فواتير'
        ordering = ['-issue_date']
    
    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.total_amount} MAD"


class OrganizationInvitation(models.Model):
    """Invitations for trainers to join an organization"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='trainer_invitations')
    email = models.EmailField()
    token = models.CharField(max_length=200, unique=True)
    
    # Invitation tracking
    invited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    accepted = models.BooleanField(default=False)
    accepted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                   related_name='accepted_org_invitations')
    accepted_at = models.DateTimeField(null=True, blank=True)
    
    # Expiration
    expires_at = models.DateTimeField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'دعوة منظمة'
        verbose_name_plural = 'دعوات المنظمة'
        unique_together = ('organization', 'email')
    
    def __str__(self):
        return f"Invitation for {self.email} to join {self.organization.name}"
    
    @property
    def is_expired(self):
        return timezone.now() > self.expires_at
    
    @property
    def is_valid(self):
        return not self.accepted and not self.is_expired


class SeatOverage(models.Model):
    """Track extra seat purchases for organizations"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='seat_overages')
    
    # Overage purchase
    seats_purchased = models.IntegerField(validators=[MinValueValidator(1)])
    price_per_seat = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Period
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'زيادة المقاعد'
        verbose_name_plural = 'زيادة المقاعد'
    
    def __str__(self):
        return f"{self.organization.name} - {self.seats_purchased} seats"
