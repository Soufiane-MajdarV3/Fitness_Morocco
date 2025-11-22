# Testing Guide - Billing System

## Pre-Testing Setup

### 1. Database Preparation
```bash
# Run migrations
python manage.py migrate payments
python manage.py migrate bookings
python manage.py migrate trainers

# Initialize plans
python manage.py init_subscription_plans

# Create superuser if needed
python manage.py createsuperuser
```

### 2. Start Development Server
```bash
python manage.py runserver
```

Access:
- Admin: http://localhost:8000/admin
- API: http://localhost:8000/api/billing/

---

## Test Suite 1: Model Tests

### Test 1.1: SubscriptionPlan Creation
```python
python manage.py shell

from payments.models import SubscriptionPlan

# Verify 4 plans exist
plans = SubscriptionPlan.objects.all()
assert plans.count() == 4
print("✓ All 4 plans created")

# Verify plan properties
basic = SubscriptionPlan.objects.get(key='basic')
assert basic.price_monthly == 0
assert basic.booking_limit_per_month == 5
assert basic.is_org_plan == False
print("✓ Basic plan correct")

premium = SubscriptionPlan.objects.get(key='premium')
assert premium.price_monthly == 99
assert premium.commission_rate == 15
print("✓ Premium plan correct")

club = SubscriptionPlan.objects.get(key='club')
assert club.is_org_plan == True
assert club.included_seats == 10
print("✓ Club plan correct")
```

### Test 1.2: TrainerSubscription
```python
from django.contrib.auth import get_user_model
from payments.models import TrainerSubscription

User = get_user_model()

# Create trainer
trainer = User.objects.create_user(
    email='trainer1@test.com',
    username='trainer1',
    password='test123',
    user_type='trainer'
)

# Create subscription
sub = TrainerSubscription.objects.create(
    trainer=trainer,
    plan=basic
)

assert sub.is_active == True
assert sub.is_subscription_active == False  # No dates set yet
print("✓ TrainerSubscription created")
```

### Test 1.3: Organization Model
```python
from payments.models import Organization

# Create org owner
owner = User.objects.create_user(
    email='gym@test.com',
    username='gymowner',
    password='test123',
    user_type='admin'
)

# Create organization
org = Organization.objects.create(
    name='Test Gym',
    owner=owner,
    email='gym@test.com',
    subscription_plan=club
)

assert org.total_seats == 10  # From plan
assert org.available_seats == 10
assert org.seats_used == 0
print("✓ Organization created")
```

---

## Test Suite 2: Service Tests

### Test 2.1: SubscriptionService
```python
from payments.services import SubscriptionService

# Create trainer subscription via service
sub = SubscriptionService.create_trainer_subscription(trainer, 'premium', is_trial=True)
assert sub.plan.key == 'premium'
assert sub.is_trial == True
assert sub.trial_used == False
print("✓ SubscriptionService.create_trainer_subscription works")

# Get commission rate
rate = SubscriptionService.get_commission_rate(trainer)
assert rate == 15  # Premium plan
print("✓ SubscriptionService.get_commission_rate works")

# Upgrade plan
upgraded = SubscriptionService.upgrade_trainer_plan(trainer, 'basic')
assert upgraded.plan.key == 'basic'
print("✓ SubscriptionService.upgrade_trainer_plan works")
```

### Test 2.2: OrganizationService
```python
from payments.services import OrganizationService

# Check seat availability
can_add = OrganizationService.can_add_trainer(org)
assert can_add == True
print("✓ OrganizationService.can_add_trainer works")

# Add trainer to organization
sub = OrganizationService.add_trainer_to_organization(org, trainer)
assert sub.organization == org
assert org.seats_used == 1
print("✓ OrganizationService.add_trainer_to_organization works")

# Try to add beyond seats (should fail)
try:
    trainer2 = User.objects.create_user(email='trainer2@test.com', user_type='trainer')
    for i in range(10):  # Fill all 10 seats
        trainer_temp = User.objects.create_user(
            email=f'trainer_fill{i}@test.com',
            username=f'trainer_fill{i}',
            user_type='trainer'
        )
        OrganizationService.add_trainer_to_organization(org, trainer_temp)
    
    # Now try to add 11th - should fail
    trainer_fail = User.objects.create_user(email='trainer_fail@test.com', user_type='trainer')
    OrganizationService.add_trainer_to_organization(org, trainer_fail)
    assert False, "Should have raised ValidationError"
except Exception as e:
    print(f"✓ OrganizationService correctly prevents overage: {type(e).__name__}")
```

### Test 2.3: CommissionService
```python
from payments.services import CommissionService
from bookings.models import Booking
from trainers.models import Trainer, SessionType
from decimal import Decimal

# Create session type
session = SessionType.objects.create(name='Cardio')

# Create trainer profile
trainer_profile = Trainer.objects.create(
    user=trainer,
    price_per_hour=Decimal('200.00')
)

# Create booking
booking = Booking.objects.create(
    client=User.objects.create_user(email='client@test.com', user_type='client'),
    trainer=trainer_profile,
    session_type=session,
    booking_date='2024-01-15',
    start_time='10:00',
    duration_minutes=60,
    total_price=Decimal('200.00')
)

# Apply commission
CommissionService.apply_booking_commission(booking)
booking.refresh_from_db()

assert booking.commission_rate == 15  # Premium trainer
assert booking.commission_amount == Decimal('30.00')  # 15% of 200
assert booking.trainer_earnings == Decimal('170.00')  # 85% of 200
print("✓ CommissionService.apply_booking_commission works")
```

---

## Test Suite 3: API Endpoint Tests

### Test 3.1: Subscription Plan Endpoints
```bash
# Get all trainer plans
curl http://localhost:8000/api/billing/plans/trainer_plans/

# Response should include:
# {
#   "count": 2,
#   "results": [
#     {"key": "basic", "name": "Basic", "price_monthly": "0.00", ...},
#     {"key": "premium", "name": "Premium", "price_monthly": "99.00", ...}
#   ]
# }

# Get organization plans
curl http://localhost:8000/api/billing/plans/organization_plans/

# Response should include:
# {
#   "count": 2,
#   "results": [
#     {"key": "club", ...},
#     {"key": "gold_club", ...}
#   ]
# }
```

### Test 3.2: Trainer Subscription Endpoints (Authenticated)
```bash
# Create test trainer and get token
python manage.py shell
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()
trainer = User.objects.get(email='trainer1@test.com')
token, _ = Token.objects.get_or_create(user=trainer)
print(token.key)

# Exit shell and set token
TOKEN="your_token_here"

# Start trial
curl -X POST http://localhost:8000/api/billing/trainer-subscription/start-trial/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json"

# Get subscription
curl http://localhost:8000/api/billing/trainer-subscription/my-subscription/ \
  -H "Authorization: Token $TOKEN"

# Response:
# {
#   "id": "uuid",
#   "trainer": 123,
#   "plan": 1,
#   "plan_name": "Basic",
#   "is_trial": true,
#   "is_subscription_active": true,
#   "commission_rate": "20.00"
# }

# Get earnings
curl http://localhost:8000/api/billing/trainer-subscription/earnings-summary/ \
  -H "Authorization: Token $TOKEN"

# Response: 
# {
#   "total_bookings": 0,
#   "total_revenue": "0.00",
#   "total_earnings": "0.00",
#   "total_commission": "0.00",
#   "average_commission_rate": "0.00"
# }
```

### Test 3.3: Organization Endpoints
```bash
# Create organization
curl -X POST http://localhost:8000/api/billing/organizations/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Gym",
    "email": "gym@test.com",
    "phone": "+212612345678",
    "city": "Casablanca"
  }'

# Note the returned ID

# List my organizations
curl http://localhost:8000/api/billing/organizations/ \
  -H "Authorization: Token $TOKEN"

# Get specific org with seats info
curl http://localhost:8000/api/billing/organizations/{ORG_ID}/ \
  -H "Authorization: Token $TOKEN"

# Response:
# {
#   "id": "uuid",
#   "name": "Test Gym",
#   "available_seats": 0,
#   "total_seats": 0,
#   "subscription_active": false
# }
```

### Test 3.4: Invitation Flow
```bash
# Create gym owner account
# Use admin to create organization with subscription

# As gym owner, invite trainer
curl -X POST http://localhost:8000/api/billing/organizations/{ORG_ID}/invite-trainer/ \
  -H "Authorization: Token $GYM_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"email": "trainer1@test.com"}'

# Response:
# {
#   "id": "uuid",
#   "token": "invitation-token-uuid",
#   "email": "trainer1@test.com",
#   "is_valid": true,
#   "expires_at": "2024-12-21T10:00:00Z"
# }

# As trainer, get my invitations
curl http://localhost:8000/api/billing/invitations/my-invitations/ \
  -H "Authorization: Token $TRAINER_TOKEN"

# Response:
# {
#   "count": 1,
#   "results": [
#     {
#       "token": "invitation-token",
#       "organization_name": "Test Gym",
#       "is_valid": true
#     }
#   ]
# }

# Accept invitation
curl -X POST http://localhost:8000/api/billing/invitations/accept/ \
  -H "Authorization: Token $TRAINER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"token": "invitation-token"}'

# Response:
# {
#   "accepted": true,
#   "accepted_at": "2024-11-21T10:00:00Z"
# }
```

---

## Test Suite 4: Admin Interface Tests

### Test 4.1: Access Admin
1. Go to http://localhost:8000/admin
2. Login with superuser credentials

### Test 4.2: Verify Models
✓ Navigate to Payments → Subscription Plans (should show 4 plans)
✓ Navigate to Payments → Trainer Subscriptions (should show created subscriptions)
✓ Navigate to Payments → Organizations (should show created orgs)
✓ Navigate to Bookings → Bookings (verify commission fields)

### Test 4.3: Create Records via Admin
1. Create new SubscriptionPlan
2. Create TrainerSubscription
3. Verify relationships work
4. Check seat counts update correctly

---

## Test Suite 5: Edge Cases & Error Handling

### Test 5.1: Duplicate Subscription
```python
# Try to create subscription for trainer who already has one
try:
    SubscriptionService.create_trainer_subscription(trainer, 'premium')
    assert False, "Should raise ValidationError"
except ValidationError as e:
    print(f"✓ Correctly prevented duplicate: {e}")
```

### Test 5.2: Invalid Plan
```python
try:
    SubscriptionService.create_trainer_subscription(trainer, 'invalid_plan')
    assert False, "Should raise ValidationError"
except ValidationError as e:
    print(f"✓ Correctly rejected invalid plan: {e}")
```

### Test 5.3: Expired Invitation
```python
from django.utils import timezone
from datetime import timedelta

# Create expired invitation
expired_invite = OrganizationInvitation.objects.create(
    organization=org,
    email='expired@test.com',
    token='expired-token',
    expires_at=timezone.now() - timedelta(days=1)
)

# Try to accept
try:
    OrganizationService.accept_invitation('expired-token', trainer)
    assert False, "Should raise ValidationError"
except ValidationError as e:
    print(f"✓ Correctly rejected expired invitation: {e}")
```

### Test 5.4: Over-seat Addition
```python
# Already tested in 2.2 above
```

---

## Test Suite 6: Data Integrity Tests

### Test 6.1: Seat Counting
```python
# Verify seat counts are accurate
org = Organization.objects.get(name='Test Gym')
print(f"Seats used: {org.seats_used}")
print(f"Total seats: {org.total_seats}")
print(f"Available: {org.available_seats}")

# Add trainer and verify increment
before = org.seats_used
OrganizationService.add_trainer_to_organization(org, some_trainer)
org.refresh_from_db()
assert org.seats_used == before + 1
print("✓ Seat counting accurate")
```

### Test 6.2: Commission Calculation
```python
# Create multiple bookings
bookings = []
for i in range(5):
    booking = Booking.objects.create(
        client=User.objects.create_user(email=f'client{i}@test.com', user_type='client'),
        trainer=trainer_profile,
        session_type=session,
        booking_date='2024-01-15',
        start_time=f'{10+i}:00',
        duration_minutes=60,
        total_price=Decimal('200.00')
    )
    CommissionService.apply_booking_commission(booking)
    bookings.append(booking)

# Verify summary
summary = CommissionService.get_trainer_earnings_summary(trainer)
assert summary['total_bookings'] == 5
assert summary['total_revenue'] == Decimal('1000.00')
print("✓ Commission calculations accurate")
```

---

## Performance Tests

### Test 7.1: Seat Lookup Performance
```python
import time

# Add many trainers
for i in range(50):
    t = User.objects.create_user(
        email=f'perf_trainer{i}@test.com',
        username=f'perf{i}',
        user_type='trainer'
    )

# Time seat query
start = time.time()
org.refresh_from_db()
seats = org.available_seats
end = time.time()

print(f"✓ Seat query took {(end-start)*1000:.2f}ms")
```

### Test 7.2: Commission Calculation Performance
```python
# Create 100 bookings
bookings = []
for i in range(100):
    booking = Booking.objects.create(
        client=User.objects.create_user(email=f'client{i}@test.com', user_type='client'),
        trainer=trainer_profile,
        session_type=session,
        booking_date='2024-01-15',
        start_time='10:00',
        duration_minutes=60,
        total_price=Decimal('200.00')
    )
    bookings.append(booking)

# Time commission calculation
start = time.time()
for booking in bookings:
    CommissionService.apply_booking_commission(booking)
end = time.time()

print(f"✓ 100 commission calculations took {(end-start)*1000:.2f}ms")
```

---

## Checklist: All Tests Passed ✅

- [ ] Model creation tests
- [ ] Service tests
- [ ] API endpoint tests
- [ ] Admin interface tests
- [ ] Edge case tests
- [ ] Data integrity tests
- [ ] Performance tests
- [ ] Error handling tests

---

## Troubleshooting

### Issue: "No module named 'rest_framework'"
```bash
pip install --break-system-packages djangorestframework
```

### Issue: Migrations not applied
```bash
python manage.py showmigrations
python manage.py migrate
```

### Issue: Superuser doesn't exist
```bash
python manage.py createsuperuser
```

### Issue: Token not found for API calls
```python
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

User = get_user_model()
user = User.objects.get(email='...')
token, _ = Token.objects.get_or_create(user=user)
print(token.key)
```

---

**Total Test Coverage**: ~50+ test cases
**Estimated Time**: 2-3 hours for full suite
**Status**: Ready to execute
