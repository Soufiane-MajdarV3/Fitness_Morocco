# Fitness Morocco - Subscription Billing System Implementation Guide

## Overview

This document describes the complete subscription billing system implementation for the Fitness Morocco platform, supporting both individual trainers and gym/organization accounts with multi-tiered pricing, commission tracking, and Stripe integration.

## Architecture

### Database Models

#### 1. **SubscriptionPlan**
- Stores all available subscription tiers (Basic, Premium, Club, Gold Club)
- Fields:
  - `key`: Unique identifier (basic, premium, club, gold_club)
  - `name`: Display name
  - `price_monthly`: Monthly price in MAD
  - `price_annual`: Annual price (optional discount)
  - `is_org_plan`: Boolean - differentiates trainer vs gym plans
  - `included_seats`: For org plans only - number of included trainer seats
  - `overage_price_per_seat`: Extra seat cost
  - `features`: JSONField list of feature strings
  - `booking_limit_per_month`: Booking limit (null = unlimited)
  - `commission_rate`: Platform commission percentage (20% default)
  - `trial_days`: Trial duration in days (14 default)

#### 2. **TrainerSubscription**
- Individual trainer subscription records
- Links trainer to a plan and optionally to an organization
- Fields:
  - `trainer`: OneToOneField to User
  - `plan`: ForeignKey to SubscriptionPlan
  - `organization`: Optional ForeignKey to Organization
  - `is_trial`: Boolean - trial status
  - `trial_start/end`: Trial period dates
  - `trial_used`: Has trainer already used free trial?
  - `subscription_start/end`: Paid subscription period
  - `auto_renew`: Auto-renewal flag
  - `is_active`: Active status

#### 3. **Organization**
- Gym/club organization accounts
- Fields:
  - `owner`: ForeignKey to User
  - `subscription_plan`: Current org plan
  - `seats_used`: Count of trainers currently linked
  - `extra_seats_purchased`: Additional seats beyond plan
  - `subscription_start/end`: Current subscription period
  - `is_trial`: Trial status
  - Properties:
    - `available_seats`: Calculated - total_seats - seats_used
    - `total_seats`: Calculated - included_seats + extra_seats_purchased
    - `is_subscription_active`: Check if subscription valid

#### 4. **BillingSubscription**
- Stripe/payment provider subscription record
- Links to either TrainerSubscription or Organization
- Fields:
  - `trainer_subscription`: Optional link to trainer sub
  - `organization`: Optional link to org
  - `provider`: Payment provider (stripe, paypal, cmi)
  - `provider_subscription_id`: Stripe subscription ID
  - `provider_customer_id`: Stripe customer ID
  - `status`: active, trial, past_due, cancelled, ended
  - `current_period_start/end`: Billing period dates
  - `failed_payment_count`: Track payment failures

#### 5. **OrganizationInvitation**
- Invitations for trainers to join organizations
- Fields:
  - `organization`: Target org
  - `email`: Invited trainer email
  - `token`: Unique invitation token (UUID)
  - `accepted`: Boolean
  - `expires_at`: Token expiration (7 days)
  - Properties:
    - `is_expired`: Check if invitation expired
    - `is_valid`: Check if invitation valid and not accepted

#### 6. **Invoice**
- Subscription invoice records
- Fields:
  - `invoice_number`: Unique invoice number
  - `billing_subscription`: Associated billing record
  - `subtotal`: Amount before tax
  - `tax_amount`: VAT/tax
  - `total_amount`: Final amount
  - `status`: draft, sent, paid, past_due, cancelled, refunded
  - `period_start/end`: Billing period covered
  - `due_date`: Payment due date

#### 7. **SeatOverage**
- Track extra seat purchases
- Fields:
  - `organization`: Target org
  - `seats_purchased`: Number of extra seats
  - `price_per_seat`: Unit price
  - `total_price`: Total amount
  - `start_date/end_date`: Overage period

### Key Services

#### **SubscriptionService** (`payments/services.py`)
```python
# Create trainer subscription
subscription = SubscriptionService.create_trainer_subscription(
    user, 'premium', is_trial=True
)

# Upgrade trainer plan
subscription = SubscriptionService.upgrade_trainer_plan(user, 'premium')

# Get commission rate for trainer
rate = SubscriptionService.get_commission_rate(user)  # Returns Decimal

# Calculate prorated price when upgrading mid-cycle
price = SubscriptionService.calculate_prorated_price(
    current_plan, new_plan, days_remaining
)
```

#### **OrganizationService** (`payments/services.py`)
```python
# Create organization
org = OrganizationService.create_organization(owner, 'Gym Name', 'email@gym.com', 'club')

# Check seat availability
can_add = OrganizationService.can_add_trainer(org)  # Boolean

# Add trainer to organization
sub = OrganizationService.add_trainer_to_organization(org, trainer_user)

# Remove trainer
OrganizationService.remove_trainer_from_organization(org, trainer_user)

# Invite trainer
invitation = OrganizationService.invite_trainer(org, 'trainer@email.com', invited_by_user)

# Accept invitation
invitation = OrganizationService.accept_invitation(token, trainer_user)

# Purchase extra seats
overage, total = OrganizationService.purchase_extra_seats(org, num_seats=5)

# Upgrade organization plan
org = OrganizationService.upgrade_organization_plan(org, 'gold_club')
```

#### **CommissionService** (`payments/services.py`)
```python
# Calculate commission for booking
booking = CommissionService.calculate_booking_commission(booking)
# Sets: booking.commission_rate, booking.commission_amount, booking.trainer_earnings

# Get trainer earnings summary
summary = CommissionService.get_trainer_earnings_summary(
    trainer_user,
    start_date='2024-01-01',
    end_date='2024-01-31'
)
# Returns: {
#     'total_bookings': int,
#     'total_revenue': Decimal,
#     'total_earnings': Decimal,
#     'total_commission': Decimal,
#     'average_commission_rate': Decimal
# }
```

#### **StripeService** (`payments/stripe_handler.py`)
```python
# Create Stripe customer
customer_id = StripeService.create_customer(trainer_or_org, email='test@email.com')

# Create Stripe subscription
sub = StripeService.create_subscription(trainer_or_org, plan, customer_id, trial_days=14)

# Update subscription to new plan (with proration)
sub = StripeService.update_subscription(stripe_sub_id, new_plan)

# Cancel subscription
sub = StripeService.cancel_subscription(stripe_sub_id)
```

## API Endpoints

### Subscription Plans (Public)
```
GET /api/billing/plans/                    # List all active plans
GET /api/billing/plans/trainer_plans/      # List trainer plans only
GET /api/billing/plans/organization_plans/ # List org plans only
```

### Trainer Subscription
```
GET  /api/billing/trainer-subscription/my-subscription/         # Get current subscription
POST /api/billing/trainer-subscription/start-trial/             # Start free trial
POST /api/billing/trainer-subscription/upgrade-plan/            # Upgrade plan
    {
        "plan_key": "premium"
    }
POST /api/billing/trainer-subscription/cancel/                  # Cancel subscription
GET  /api/billing/trainer-subscription/earnings-summary/        # Get earnings
    ?start_date=2024-01-01&end_date=2024-01-31
```

### Organizations
```
GET    /api/billing/organizations/                    # List my organization
POST   /api/billing/organizations/                    # Create new organization
    {
        "name": "Gym Name",
        "email": "gym@email.com",
        "plan_key": "club"
    }
PATCH  /api/billing/organizations/{id}/               # Update organization
GET    /api/billing/organizations/{id}/trainers/      # List organization trainers
POST   /api/billing/organizations/{id}/invite-trainer/ # Invite trainer
    {
        "email": "trainer@email.com"
    }
POST   /api/billing/organizations/{id}/remove-trainer/ # Remove trainer
    {
        "trainer_id": 123
    }
POST   /api/billing/organizations/{id}/purchase-seats/ # Buy extra seats
    {
        "num_seats": 5
    }
POST   /api/billing/organizations/{id}/upgrade-plan/   # Upgrade org plan
    {
        "plan_key": "gold_club"
    }
```

### Organization Invitations
```
GET  /api/billing/invitations/my-invitations/    # Get pending invitations
POST /api/billing/invitations/accept/             # Accept invitation
    {
        "token": "uuid-token"
    }
```

### Invoices (Read-only)
```
GET /api/billing/invoices/                # List my invoices
GET /api/billing/invoices/{id}/download/  # Download invoice PDF (TODO)
```

## Stripe Integration

### Webhook Setup
1. Add Stripe secret to environment: `STRIPE_WEBHOOK_SECRET`
2. Configure webhook endpoint: `/api/billing/webhooks/stripe/`
3. Subscribe to events:
   - `customer.subscription.updated`
   - `invoice.payment_failed`
   - `invoice.payment_succeeded`
   - `customer.subscription.deleted`

### Webhook Handlers
- **subscription.updated**: Update BillingSubscription status
- **invoice.payment_failed**: Increment failed_payment_count, set status to past_due
- **invoice.payment_succeeded**: Create Invoice record, reset failed count
- **subscription.deleted**: Set status to cancelled

## Booking Commission Implementation

The `Booking` model now includes commission tracking:
```python
booking.commission_rate = Decimal('20')      # From trainer's plan
booking.commission_amount = Decimal('200')   # 20% of total_price
booking.trainer_earnings = Decimal('800')    # 80% of total_price
booking.organization = org                    # Link to gym if trainer in organization
```

When a booking is created:
```python
from payments.services import CommissionService

booking = Booking.objects.create(...)
CommissionService.apply_booking_commission(booking)
```

## Setup Instructions

### 1. Run Migrations
```bash
python manage.py migrate payments
python manage.py migrate bookings
python manage.py migrate trainers
```

### 2. Initialize Plans
```bash
python manage.py init_subscription_plans
```

This creates:
- **Basic**: Free, 5 bookings/month, 20% commission
- **Premium**: 99 MAD/month, unlimited bookings, 15% commission
- **Club**: 500 MAD/month, 10 trainer seats, 15% commission
- **Gold Club**: 1,200 MAD/month, 50 trainer seats, 12% commission

### 3. Configure Stripe (`.env`)
```
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_test_...
```

### 4. Create Admin Users & Test Data
```bash
# In Django shell
from django.contrib.auth import get_user_model
from payments.models import Organization, SubscriptionPlan
from payments.services import SubscriptionService, OrganizationService

User = get_user_model()

# Create test trainer
trainer = User.objects.create_user(
    email='trainer@test.com',
    username='trainer',
    password='test123',
    user_type='trainer',
    first_name='Test',
    last_name='Trainer'
)

# Create subscription
sub = SubscriptionService.create_trainer_subscription(trainer, 'basic', is_trial=True)

# Create test gym owner
gym_owner = User.objects.create_user(
    email='gym@test.com',
    username='gym_owner',
    password='test123',
    user_type='admin',
    first_name='Gym',
    last_name='Owner'
)

# Create organization
org = OrganizationService.create_organization(
    gym_owner, 'Test Gym', 'gym@test.com', 'club'
)

# Invite trainer
invite = OrganizationService.invite_trainer(org, trainer.email, gym_owner)
print(f"Invitation token: {invite.token}")

# Accept invitation
OrganizationService.accept_invitation(invite.token, trainer)
```

## Testing Flows

### Trainer Sign-up Flow
1. User signs up → Creates basic free subscription
2. User upgrades to Premium → Calls upgrade endpoint → Stripe creates subscription
3. User cancels → Sets is_active=False

### Gym Creation Flow
1. Gym owner creates organization → Enters trial
2. Owner invites trainers → Creates invitation tokens
3. Trainers accept → Linked to organization, seats_used incremented
4. Gym hits seat limit → Call purchase_seats endpoint
5. Extra seats auto-added to org

### Booking Commission Flow
1. Client books trainer → Creates Booking
2. Apply commission → Sets commission_rate, commission_amount, trainer_earnings
3. Booking completed → Payment processed
4. Trainer earnings updated → Displayed in dashboard

## Security Considerations

✓ Seat enforcement server-side (cannot add trainer beyond seats)
✓ Invitation tokens time-limited (7 days)
✓ Webhook signature validation
✓ Rate limiting on invite endpoints
✓ Only see own subscriptions/invoices
✓ Only org owner can manage organization

## Admin Interface

All models registered in Django admin with custom actions:
- View plan features
- Manage organization trainers
- Override seats manually
- Issue manual invoices
- View payment history
- Manage invitations

## Future Enhancements

- [ ] PDF invoice generation & email delivery
- [ ] Email notifications for payment failures
- [ ] Automated dunning (retry) logic
- [ ] Refund management interface
- [ ] Usage-based billing for overages
- [ ] Annual billing discount automation
- [ ] Revenue analytics dashboard
- [ ] Multi-currency support
- [ ] Local payment gateway (CMI) integration

## Pricing Summary

| Plan | Price | Bookings | Commission | Features |
|------|-------|----------|-----------|----------|
| Basic | Free | 5/month | 20% | Basic profile |
| Premium | 99 MAD/mo | Unlimited | 15% | Featured listing, priority support |
| Club | 500 MAD/mo | Unlimited | 15% | 10 trainer seats, team dashboard |
| Gold Club | 1,200 MAD/mo | Unlimited | 12% | 50 seats, API access, account manager |

## Contact & Support

For questions or issues with the billing system, contact the development team.
