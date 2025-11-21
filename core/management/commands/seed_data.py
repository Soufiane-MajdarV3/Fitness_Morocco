"""
Management command to seed initial data into the database.
Run with: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from trainers.models import City, SessionType, Trainer, SubscriptionPlan
from clients.models import ClientProfile
from bookings.models import Booking, Review
from datetime import datetime, timedelta
from decimal import Decimal

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed the database with initial data'
    
    def handle(self, *args, **options):
        self.stdout.write('Creating cities...')
        cities = []
        city_names = ['الدار البيضاء', 'فاس', 'مراكش', 'تطوان', 'أكادير', 'الرباط']
        for name in city_names:
            city, _ = City.objects.get_or_create(
                name=name,
                defaults={'code': name[:3]}
            )
            cities.append(city)
        
        self.stdout.write('Creating session types...')
        session_types = []
        session_type_names = [
            ('اللياقة البدنية', 'fa-dumbbell'),
            ('اليوغا', 'fa-spa'),
            ('الملاكمة', 'fa-hand-fist'),
            ('السباحة', 'fa-person-swimming'),
            ('كروس فت', 'fa-fire'),
            ('تغذية', 'fa-apple-alt'),
        ]
        for name, icon in session_type_names:
            session_type, _ = SessionType.objects.get_or_create(
                name=name,
                defaults={'icon': icon}
            )
            session_types.append(session_type)
        
        self.stdout.write('Creating subscription plans...')
        plans = [
            ('ذهبي', 'gold', 99.99, 4),
            ('بلاتيني', 'platinum', 199.99, 8),
            ('ماسي', 'diamond', 299.99, 16),
        ]
        for name, plan_type, price, sessions in plans:
            SubscriptionPlan.objects.get_or_create(
                plan_type=plan_type,
                defaults={
                    'name': name,
                    'price_monthly': Decimal(price),
                    'sessions_per_month': sessions,
                }
            )
        
        self.stdout.write('Creating trainers...')
        trainer_data = [
            ('Ahmed', 'Hassan', 'ahmed@trainers.com', 'male', 'Dammam', 5, 150),
            ('Fatima', 'Ali', 'fatima@trainers.com', 'female', 'Fez', 3, 120),
            ('Mohamed', 'Ibrahim', 'mohamed@trainers.com', 'male', 'Marrakech', 7, 180),
            ('Layla', 'Mohammed', 'layla@trainers.com', 'female', 'Tetouan', 4, 130),
            ('Karim', 'Salah', 'karim@trainers.com', 'male', 'Agadir', 6, 160),
        ]
        
        trainers = []
        for i, (first_name, last_name, email, gender, city, exp, price) in enumerate(trainer_data):
            username = f'trainer{i+1}'
            user, _ = User.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'user_type': 'trainer',
                    'city': city,
                    'is_verified': True,
                }
            )
            
            trainer, _ = Trainer.objects.get_or_create(
                user=user,
                defaults={
                    'experience_years': exp,
                    'price_per_hour': Decimal(price),
                    'is_approved': True,
                    'rating': 4.5 + (i % 3) * 0.3,
                }
            )
            
            # Add specialties
            trainer.specialties.add(*session_types[:3])
            trainers.append(trainer)
        
        self.stdout.write('Creating clients...')
        clients = []
        for i in range(20):
            username = f'client{i+1}'
            user, _ = User.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': f'Client{i+1}',
                    'last_name': 'Test',
                    'email': f'client{i+1}@example.com',
                    'user_type': 'client',
                    'city': cities[i % len(cities)].name,
                    'is_verified': True,
                }
            )
            
            client_profile, _ = ClientProfile.objects.get_or_create(
                user=user,
                defaults={
                    'age': 25 + (i % 20),
                    'fitness_level': ['beginner', 'intermediate', 'advanced'][i % 3],
                    'weight': 70.0 + (i % 10),
                    'height': 170 + (i % 10),
                }
            )
            clients.append(user)
        
        self.stdout.write('Creating bookings and reviews...')
        for i, trainer in enumerate(trainers):
            for j in range(3):
                client = clients[(i * 3 + j) % len(clients)]
                booking_date = datetime.now().date() - timedelta(days=10 - j*3)
                
                booking, _ = Booking.objects.get_or_create(
                    client=client,
                    trainer=trainer,
                    booking_date=booking_date,
                    start_time=f'{9+j}:00',
                    defaults={
                        'session_type': session_types[0],
                        'duration_minutes': 60,
                        'total_price': trainer.price_per_hour,
                        'status': 'completed',
                    }
                )
                
                # Add review
                Review.objects.get_or_create(
                    booking=booking,
                    defaults={
                        'trainer': trainer,
                        'client': client,
                        'rating': 4 + (i % 2),
                        'comment': f'جلسة رائعة مع {trainer.user.get_full_name()}!',
                    }
                )
        
        self.stdout.write(self.style.SUCCESS('Data seeding completed successfully!'))