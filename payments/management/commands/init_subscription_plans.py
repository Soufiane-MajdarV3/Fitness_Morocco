"""
Django management command to initialize subscription plans
Usage: python manage.py init_subscription_plans
"""
from django.core.management.base import BaseCommand
from payments.models import SubscriptionPlan
from decimal import Decimal


class Command(BaseCommand):
    help = 'Initialize default subscription plans'

    def handle(self, *args, **options):
        plans_data = [
            {
                'key': 'basic',
                'name': 'Basic',
                'description': 'Free plan for individual trainers',
                'price_monthly': Decimal('0.00'),
                'price_annual': Decimal('0.00'),
                'is_org_plan': False,
                'booking_limit_per_month': 5,
                'commission_rate': Decimal('20'),
                'trial_days': 14,
                'features': [
                    'Profile visibility (basic)',
                    'Up to 5 active bookings per month',
                    'Basic search ranking',
                    'Profile page',
                    'Calendar',
                    'Basic analytics (last 30 days)'
                ]
            },
            {
                'key': 'premium',
                'name': 'Premium',
                'description': 'Premium plan for individual trainers',
                'price_monthly': Decimal('99.00'),
                'price_annual': Decimal('990.00'),
                'is_org_plan': False,
                'booking_limit_per_month': None,  # Unlimited
                'commission_rate': Decimal('15'),
                'trial_days': 14,
                'features': [
                    'Featured listing in search',
                    'Unlimited bookings',
                    'Advanced analytics',
                    'Priority support',
                    'Reduced commission fee (15% vs 20%)',
                    'Promotional credits (1 boosted slot per month)',
                    'Priority customer leads'
                ]
            },
            {
                'key': 'club',
                'name': 'Club Plan',
                'description': 'Organization plan for gyms/clubs',
                'price_monthly': Decimal('500.00'),
                'price_annual': Decimal('5000.00'),
                'is_org_plan': True,
                'included_seats': 10,
                'overage_price_per_seat': Decimal('60.00'),
                'commission_rate': Decimal('15'),
                'trial_days': 14,
                'features': [
                    'Team management dashboard',
                    'Invite trainers (accounts created or linked)',
                    'Central billing',
                    'Gym page/listing',
                    'Priority customer leads',
                    'Per-seat admin controls',
                    'One free premium trainer slot',
                    'Up to 10 trainer seats'
                ]
            },
            {
                'key': 'gold_club',
                'name': 'Gold Club Plan',
                'description': 'Premium organization plan for large gyms',
                'price_monthly': Decimal('1200.00'),
                'price_annual': Decimal('12000.00'),
                'is_org_plan': True,
                'included_seats': 50,
                'overage_price_per_seat': Decimal('40.00'),
                'commission_rate': Decimal('12'),
                'trial_days': 14,
                'features': [
                    'Team management dashboard (advanced)',
                    'All Club features',
                    'Advanced analytics & campaigns',
                    'Bulk messaging to clients',
                    'API access',
                    'Dedicated account manager',
                    'Priority onboarding & verification',
                    'Up to 50 trainer seats'
                ]
            }
        ]

        for plan_data in plans_data:
            plan, created = SubscriptionPlan.objects.get_or_create(
                key=plan_data['key'],
                defaults=plan_data
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created plan: {plan.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⚠ Plan already exists: {plan.name}')
                )

        self.stdout.write(
            self.style.SUCCESS('\n✓ All subscription plans initialized successfully!')
        )
