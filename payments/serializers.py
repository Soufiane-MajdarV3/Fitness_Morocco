"""
DRF Serializers for subscription and billing models
"""
from rest_framework import serializers
from .models import (
    SubscriptionPlan, Organization, TrainerSubscription, BillingSubscription,
    OrganizationInvitation, Invoice, SeatOverage
)
from django.contrib.auth import get_user_model

User = get_user_model()


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = (
            'id', 'key', 'name', 'description', 'price_monthly', 'price_annual',
            'is_org_plan', 'included_seats', 'overage_price_per_seat', 'features',
            'booking_limit_per_month', 'commission_rate', 'trial_days', 'is_trial_available'
        )
        read_only_fields = ('id',)


class TrainerSubscriptionSerializer(serializers.ModelSerializer):
    trainer_email = serializers.CharField(source='trainer.email', read_only=True)
    plan_name = serializers.CharField(source='plan.name', read_only=True)
    organization_name = serializers.CharField(source='organization.name', read_only=True)
    commission_rate = serializers.SerializerMethodField()
    
    class Meta:
        model = TrainerSubscription
        fields = (
            'id', 'trainer', 'trainer_email', 'plan', 'plan_name', 'organization',
            'organization_name', 'is_trial', 'trial_start', 'trial_end', 'trial_used',
            'subscription_start', 'subscription_end', 'is_active', 'auto_renew',
            'is_subscription_active', 'commission_rate', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at', 'is_subscription_active')
    
    def get_commission_rate(self, obj):
        return str(obj.commission_rate)


class OrganizationSerializer(serializers.ModelSerializer):
    owner_email = serializers.CharField(source='owner.email', read_only=True)
    available_seats = serializers.SerializerMethodField()
    total_seats = serializers.SerializerMethodField()
    subscription_active = serializers.SerializerMethodField()
    
    class Meta:
        model = Organization
        fields = (
            'id', 'name', 'owner', 'owner_email', 'subscription_plan', 'subscription_start',
            'subscription_end', 'is_trial', 'trial_start', 'trial_end', 'seats_used',
            'extra_seats_purchased', 'available_seats', 'total_seats', 'email', 'phone',
            'city', 'address', 'description', 'logo', 'website', 'is_active', 'is_verified',
            'subscription_active', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at', 'seats_used')
    
    def get_available_seats(self, obj):
        return obj.available_seats
    
    def get_total_seats(self, obj):
        return obj.total_seats
    
    def get_subscription_active(self, obj):
        return obj.is_subscription_active


class OrganizationInvitationSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source='organization.name', read_only=True)
    invited_by_email = serializers.CharField(source='invited_by.email', read_only=True)
    is_valid = serializers.SerializerMethodField()
    
    class Meta:
        model = OrganizationInvitation
        fields = (
            'id', 'organization', 'organization_name', 'email', 'token', 'invited_by',
            'invited_by_email', 'accepted', 'accepted_by', 'accepted_at', 'expires_at',
            'is_valid', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'token', 'created_at', 'updated_at', 'accepted_by', 'accepted_at')
    
    def get_is_valid(self, obj):
        return obj.is_valid


class BillingSubscriptionSerializer(serializers.ModelSerializer):
    trainer_email = serializers.SerializerMethodField()
    organization_name = serializers.SerializerMethodField()
    plan_name = serializers.CharField(source='plan.name', read_only=True)
    
    class Meta:
        model = BillingSubscription
        fields = (
            'id', 'trainer_subscription', 'organization', 'trainer_email', 'organization_name',
            'provider', 'provider_subscription_id', 'provider_customer_id', 'plan', 'plan_name',
            'billing_period', 'status', 'current_period_start', 'current_period_end', 'trial_start',
            'trial_end', 'cancelled_at', 'failed_payment_count', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def get_trainer_email(self, obj):
        if obj.trainer_subscription:
            return obj.trainer_subscription.trainer.email
        return None
    
    def get_organization_name(self, obj):
        if obj.organization:
            return obj.organization.name
        return None


class InvoiceSerializer(serializers.ModelSerializer):
    organization_name = serializers.SerializerMethodField()
    trainer_email = serializers.SerializerMethodField()
    
    class Meta:
        model = Invoice
        fields = (
            'id', 'invoice_number', 'provider_invoice_id', 'organization_name', 'trainer_email',
            'subtotal', 'tax_amount', 'total_amount', 'status', 'issue_date', 'due_date',
            'paid_date', 'period_start', 'period_end', 'notes', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def get_organization_name(self, obj):
        if obj.organization:
            return obj.organization.name
        return None
    
    def get_trainer_email(self, obj):
        if obj.trainer_subscription:
            return obj.trainer_subscription.trainer.email
        return None


class SeatOverageSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source='organization.name', read_only=True)
    
    class Meta:
        model = SeatOverage
        fields = (
            'id', 'organization', 'organization_name', 'seats_purchased', 'price_per_seat',
            'total_price', 'start_date', 'end_date', 'is_active', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')
