"""
URL Configuration for payments/billing API
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SubscriptionPlanViewSet, TrainerSubscriptionViewSet, OrganizationViewSet,
    OrganizationInvitationViewSet, InvoiceViewSet
)
from .stripe_handler import stripe_webhook

router = DefaultRouter()
router.register(r'plans', SubscriptionPlanViewSet, basename='subscription-plan')
router.register(r'organizations', OrganizationViewSet, basename='organization')
router.register(r'invoices', InvoiceViewSet, basename='invoice')

app_name = 'payments'

urlpatterns = [
    path('', include(router.urls)),
    path('trainer-subscription/', include([
        path('my-subscription/', TrainerSubscriptionViewSet.as_view({
            'get': 'my_subscription'
        }), name='trainer-my-subscription'),
        path('start-trial/', TrainerSubscriptionViewSet.as_view({
            'post': 'start_trial'
        }), name='trainer-start-trial'),
        path('upgrade-plan/', TrainerSubscriptionViewSet.as_view({
            'post': 'upgrade_plan'
        }), name='trainer-upgrade-plan'),
        path('cancel/', TrainerSubscriptionViewSet.as_view({
            'post': 'cancel'
        }), name='trainer-cancel'),
        path('earnings-summary/', TrainerSubscriptionViewSet.as_view({
            'get': 'earnings_summary'
        }), name='trainer-earnings-summary'),
    ])),
    path('invitations/', include([
        path('accept/', OrganizationInvitationViewSet.as_view({
            'post': 'accept_invitation'
        }), name='accept-invitation'),
        path('my-invitations/', OrganizationInvitationViewSet.as_view({
            'get': 'my_invitations'
        }), name='my-invitations'),
    ])),
    path('webhooks/stripe/', stripe_webhook, name='stripe-webhook'),
]
