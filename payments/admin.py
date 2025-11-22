from django.contrib import admin
from django.utils.html import format_html
from .models import (
    PaymentGatewayConfig, SubscriptionPlan, Organization, TrainerSubscription,
    BillingSubscription, Invoice, OrganizationInvitation, SeatOverage
)


@admin.register(PaymentGatewayConfig)
class PaymentGatewayConfigAdmin(admin.ModelAdmin):
    list_display = ('gateway_name', 'is_active', 'created_at')
    list_filter = ('gateway_name', 'is_active')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Gateway Info', {
            'fields': ('gateway_name', 'is_active')
        }),
        ('API Credentials', {
            'fields': ('api_key', 'secret_key', 'webhook_secret'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'key', 'price_monthly', 'price_annual', 'is_org_plan', 'is_active')
    list_filter = ('key', 'is_org_plan', 'is_active')
    fieldsets = (
        ('Plan Details', {
            'fields': ('key', 'name', 'description', 'is_org_plan')
        }),
        ('Pricing', {
            'fields': ('price_monthly', 'price_annual')
        }),
        ('Organization Settings', {
            'fields': ('included_seats', 'overage_price_per_seat'),
            'classes': ('collapse',)
        }),
        ('Features & Limits', {
            'fields': ('features', 'booking_limit_per_month', 'commission_rate')
        }),
        ('Trial', {
            'fields': ('trial_days', 'is_trial_available')
        }),
        ('Status', {
            'fields': ('is_active', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'subscription_plan', 'seats_info', 'is_subscription_active', 'is_active')
    list_filter = ('is_active', 'is_verified', 'subscription_plan')
    search_fields = ('name', 'owner__email', 'email')
    readonly_fields = ('created_at', 'updated_at')
    
    def seats_info(self, obj):
        if obj.subscription_plan:
            return f"{obj.seats_used} / {obj.total_seats} seats"
        return "No plan"
    seats_info.short_description = "Seats Used"
    
    fieldsets = (
        ('Organization Info', {
            'fields': ('name', 'owner', 'is_active', 'is_verified')
        }),
        ('Subscription', {
            'fields': ('subscription_plan', 'subscription_start', 'subscription_end', 'is_trial', 'trial_start', 'trial_end')
        }),
        ('Seats', {
            'fields': ('seats_used', 'extra_seats_purchased')
        }),
        ('Contact & Location', {
            'fields': ('email', 'phone', 'city', 'address')
        }),
        ('Additional Info', {
            'fields': ('description', 'logo', 'website')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(TrainerSubscription)
class TrainerSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('trainer_name', 'plan', 'organization', 'is_subscription_active', 'trial_used', 'is_active')
    list_filter = ('is_active', 'trial_used', 'plan', 'organization')
    search_fields = ('trainer__email', 'trainer__first_name', 'trainer__last_name')
    readonly_fields = ('created_at', 'updated_at', 'id')
    
    def trainer_name(self, obj):
        return obj.trainer.get_full_name()
    trainer_name.short_description = "Trainer"
    
    fieldsets = (
        ('Trainer Info', {
            'fields': ('id', 'trainer', 'plan', 'organization', 'is_active')
        }),
        ('Trial Status', {
            'fields': ('is_trial', 'trial_start', 'trial_end', 'trial_used')
        }),
        ('Subscription Period', {
            'fields': ('subscription_start', 'subscription_end', 'auto_renew')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(BillingSubscription)
class BillingSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('billing_id', 'provider', 'status', 'current_period_end', 'failed_payment_count')
    list_filter = ('status', 'provider', 'billing_period')
    search_fields = ('provider_subscription_id', 'provider_customer_id')
    readonly_fields = ('created_at', 'updated_at', 'id')
    
    def billing_id(self, obj):
        if obj.trainer_subscription:
            return f"Trainer: {obj.trainer_subscription.trainer.email}"
        return f"Org: {obj.organization.name}"
    billing_id.short_description = "Billing For"
    
    fieldsets = (
        ('Subscription Links', {
            'fields': ('id', 'trainer_subscription', 'organization')
        }),
        ('Provider Info', {
            'fields': ('provider', 'provider_subscription_id', 'provider_customer_id', 'payment_method_id')
        }),
        ('Plan & Status', {
            'fields': ('plan', 'billing_period', 'status')
        }),
        ('Periods', {
            'fields': ('current_period_start', 'current_period_end', 'trial_start', 'trial_end', 'cancelled_at')
        }),
        ('Payment Tracking', {
            'fields': ('failed_payment_count',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'status', 'total_amount', 'issue_date', 'due_date')
    list_filter = ('status', 'issue_date', 'billing_subscription')
    search_fields = ('invoice_number', 'provider_invoice_id')
    readonly_fields = ('created_at', 'updated_at', 'id')
    
    fieldsets = (
        ('Invoice Info', {
            'fields': ('id', 'invoice_number', 'provider_invoice_id', 'status')
        }),
        ('Related Records', {
            'fields': ('billing_subscription', 'trainer_subscription', 'organization')
        }),
        ('Amounts', {
            'fields': ('subtotal', 'tax_amount', 'total_amount')
        }),
        ('Dates', {
            'fields': ('issue_date', 'due_date', 'paid_date', 'period_start', 'period_end')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(OrganizationInvitation)
class OrganizationInvitationAdmin(admin.ModelAdmin):
    list_display = ('email', 'organization', 'accepted_status', 'expires_at', 'created_at')
    list_filter = ('accepted', 'organization', 'created_at')
    search_fields = ('email', 'organization__name')
    readonly_fields = ('created_at', 'updated_at', 'id', 'token')
    
    def accepted_status(self, obj):
        if obj.accepted:
            color = 'green'
            status = 'Accepted'
        elif obj.is_expired:
            color = 'red'
            status = 'Expired'
        else:
            color = 'orange'
            status = 'Pending'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, status
        )
    accepted_status.short_description = "Status"
    
    fieldsets = (
        ('Invitation Info', {
            'fields': ('id', 'email', 'organization', 'token')
        }),
        ('Acceptance', {
            'fields': ('accepted', 'accepted_by', 'accepted_at')
        }),
        ('Expiration', {
            'fields': ('expires_at',)
        }),
        ('Meta', {
            'fields': ('invited_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(SeatOverage)
class SeatOverageAdmin(admin.ModelAdmin):
    list_display = ('organization', 'seats_purchased', 'total_price', 'end_date', 'is_active')
    list_filter = ('is_active', 'organization', 'start_date')
    readonly_fields = ('created_at', 'updated_at', 'id')
    
    fieldsets = (
        ('Organization', {
            'fields': ('id', 'organization')
        }),
        ('Seat Overage', {
            'fields': ('seats_purchased', 'price_per_seat', 'total_price')
        }),
        ('Period', {
            'fields': ('start_date', 'end_date', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
