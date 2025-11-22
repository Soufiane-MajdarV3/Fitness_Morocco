# Billing System - Quick Start Guide

## What's Been Implemented ✅

### 1. Database Models
- ✅ **SubscriptionPlan**: Basic, Premium, Club, Gold Club plans
- ✅ **TrainerSubscription**: Individual trainer subscriptions
- ✅ **Organization**: Gym/club organization accounts
- ✅ **BillingSubscription**: Stripe integration records
- ✅ **OrganizationInvitation**: Trainer invitation system
- ✅ **Invoice**: Subscription invoice tracking
- ✅ **SeatOverage**: Extra seat purchase tracking
- ✅ **Enhanced Booking Model**: Commission tracking

### 2. Business Logic (Services)
- ✅ **SubscriptionService**: Create, upgrade, manage trainer subscriptions
- ✅ **OrganizationService**: Create orgs, invite trainers, manage seats
- ✅ **CommissionService**: Calculate commissions and earnings
- ✅ **StripeService**: Payment provider integration

### 3. REST API Endpoints
- ✅ Subscription plan listings
- ✅ Trainer subscription management
- ✅ Organization management
- ✅ Trainer invitations
- ✅ Invoice access
- ✅ Earnings summaries

### 4. Stripe Integration
- ✅ Customer creation
- ✅ Subscription management
- ✅ Webhook handlers (payment events)
- ✅ Invoice tracking

### 5. Admin Interface
- ✅ Full Django admin for all models
- ✅ Custom admin views with seat tracking
- ✅ Plan management
- ✅ Invitation management

## Setup Steps (5 minutes)

### Step 1: Install Dependencies
```bash
pip install --break-system-packages \
  djangorestframework \
  django-filter \
  stripe
```

### Step 2: Run Migrations
```bash
python manage.py migrate payments
python manage.py migrate bookings
python manage.py migrate trainers
```

### Step 3: Initialize Plans
```bash
python manage.py init_subscription_plans
```

This creates all 4 subscription tiers with proper pricing and features.

### Step 4: Configure Stripe (Optional for Testing)
Create `.env` file:
```
STRIPE_PUBLIC_KEY=pk_test_xxxx
STRIPE_SECRET_KEY=sk_test_xxxx
STRIPE_WEBHOOK_SECRET=whsec_xxxx
```

Get test keys from: https://dashboard.stripe.com/test/keys

### Step 5: Test the System
```bash
python manage.py shell
```

```python
from django.contrib.auth import get_user_model
from payments.models import SubscriptionPlan
from payments.services import SubscriptionService

User = get_user_model()

# Create test user
trainer = User.objects.create_user(
    email='test@trainer.com',
    username='testtrainer',
    password='test123',
    user_type='trainer',
    first_name='Test',
    last_name='Trainer'
)

# Check plans
plans = SubscriptionPlan.objects.all()
for plan in plans:
    print(f"{plan.name}: {plan.price_monthly} MAD/month")

# Create subscription
sub = SubscriptionService.create_trainer_subscription(trainer, 'basic', is_trial=True)
print(f"Subscription created: {sub}")

# Get commission rate
rate = SubscriptionService.get_commission_rate(trainer)
print(f"Commission rate: {rate}%")
```

## Key Features

### For Individual Trainers
1. **Automatic Basic Subscription** on signup
2. **Free 14-Day Trial** for Premium plan
3. **Upgrade/Downgrade** anytime with proration
4. **Commission Tracking** - see how much platform takes
5. **Earnings Dashboard** - view monthly earnings

### For Gyms/Clubs
1. **Team Management** - manage multiple trainers
2. **Seat-Based Pricing** - pay per trainer slot (10 or 50)
3. **Bulk Invitations** - invite trainers via email
4. **Centralized Billing** - one invoice for entire gym
5. **Extra Seats** - purchase additional slots on demand

### Payment Features
1. **14-Day Free Trial** for paid plans
2. **Stripe Integration** - secure payment processing
3. **Automatic Invoicing** - monthly invoices created
4. **Failed Payment Recovery** - retry logic built-in
5. **Commission Calculation** - automatic on bookings

## API Testing

### Test Trainer Flow
```bash
# 1. Get available plans
curl http://localhost:8000/api/billing/plans/trainer_plans/

# 2. Start free trial
curl -X POST http://localhost:8000/api/billing/trainer-subscription/start-trial/ \
  -H "Authorization: Token YOUR_TOKEN"

# 3. Get my subscription
curl http://localhost:8000/api/billing/trainer-subscription/my-subscription/ \
  -H "Authorization: Token YOUR_TOKEN"

# 4. Get earnings summary
curl http://localhost:8000/api/billing/trainer-subscription/earnings-summary/ \
  -H "Authorization: Token YOUR_TOKEN"
```

### Test Organization Flow
```bash
# 1. Create organization
curl -X POST http://localhost:8000/api/billing/organizations/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Gym",
    "email": "gym@example.com",
    "plan_key": "club"
  }'

# 2. Invite trainer
curl -X POST http://localhost:8000/api/billing/organizations/{org_id}/invite-trainer/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"email": "trainer@example.com"}'

# 3. Accept invitation (as trainer)
curl -X POST http://localhost:8000/api/billing/invitations/accept/ \
  -H "Authorization: Token TRAINER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"token": "UUID_FROM_INVITATION"}'

# 4. List trainers in org
curl http://localhost:8000/api/billing/organizations/{org_id}/trainers/ \
  -H "Authorization: Token YOUR_TOKEN"
```

## Database Schema Overview

```
User (CustomUser)
├── TrainerSubscription (OneToOne)
│   ├── SubscriptionPlan
│   └── Organization (nullable)
│
└── Organization (ForeignKey to owner)
    ├── SubscriptionPlan
    ├── TrainerSubscription (many)
    ├── OrganizationInvitation
    └── SeatOverage

BillingSubscription
├── TrainerSubscription (OneToOne)
├── Organization (OneToOne)
└── Invoice (many)

Booking (enhanced)
├── commission_rate
├── commission_amount
├── trainer_earnings
└── organization (nullable)
```

## Commission Structure

| Plan | Monthly | Booking Commission | Seats |
|------|---------|-------------------|-------|
| Basic | Free | 20% | Solo trainer |
| Premium | 99 MAD | 15% | Solo trainer |
| Club | 500 MAD | 15% | 10 trainers (+60 MAD each) |
| Gold Club | 1,200 MAD | 12% | 50 trainers (+40 MAD each) |

## Common Operations

### Creating a New Trainer Account
```python
from payments.services import SubscriptionService
from django.contrib.auth import get_user_model

User = get_user_model()

# User signs up
trainer = User.objects.create_user(...)

# Auto-create basic subscription
sub = SubscriptionService.create_trainer_subscription(trainer, 'basic', is_trial=False)
```

### Inviting Trainers to Gym
```python
from payments.services import OrganizationService

# As gym owner, invite trainer
invitation = OrganizationService.invite_trainer(
    organization, 
    'trainer@email.com', 
    gym_owner
)

# Send invitation email with: invitation.token

# Trainer accepts (from email link)
OrganizationService.accept_invitation(invitation.token, trainer_user)
```

### Calculating Booking Commission
```python
from payments.services import CommissionService

# When booking is created
booking = Booking.objects.create(...)
CommissionService.apply_booking_commission(booking)

# Now booking has:
# - commission_rate: 20% or 15% based on trainer's plan
# - commission_amount: calculated amount
# - trainer_earnings: what trainer gets
```

### Gym Purchasing Extra Seats
```python
from payments.services import OrganizationService

# Gym needs more trainers
overage, total_price = OrganizationService.purchase_extra_seats(org, 5)

# Organization.extra_seats_purchased updated
# SeatOverage record created
# Invoice should be generated for gym owner
```

## File Structure

```
payments/
├── models.py                    # All billing models
├── views.py                     # REST API viewsets
├── serializers.py               # DRF serializers
├── services.py                  # Business logic
├── stripe_handler.py            # Stripe integration
├── admin.py                     # Django admin
├── urls.py                      # API routing
├── apps.py
├── management/
│   └── commands/
│       └── init_subscription_plans.py  # Initialize plans
└── migrations/
    └── 0002_*.py               # New models migration
```

## Next Steps - Frontend UI

To build the subscription UI, you'll need:

### Trainer Subscription Pages
1. **Pricing Page** - Show all trainer plans
2. **Subscription Dashboard** - Current plan, billing date, upgrade/downgrade buttons
3. **Earnings Page** - Commission rate, lifetime earnings, monthly breakdown

### Gym Management Pages
1. **Create Organization** - Setup gym account
2. **Team Dashboard** - List trainers, seat usage, invite interface
3. **Billing Page** - Current plan, invoice history, upgrade/purchase seats

### Booking Commission Display
- Show commission breakdown in booking confirmation
- Trainer earnings visible in their dashboard

## Troubleshooting

### "ModuleNotFoundError: No module named 'rest_framework'"
```bash
pip install --break-system-packages djangorestframework
```

### Migrations not found
```bash
python manage.py makemigrations payments
python manage.py migrate
```

### Stripe webhook not working
1. Check STRIPE_WEBHOOK_SECRET in .env
2. Verify webhook URL in Stripe dashboard: `https://yourdomain.com/api/billing/webhooks/stripe/`
3. Check Django logs for webhook processing errors

## Support

Refer to `BILLING_IMPLEMENTATION.md` for detailed documentation.

---
**Implementation Date**: November 2024
**Version**: 1.0 (MVP)
**Status**: Ready for Testing
