"""
Management command to populate the database with realistic seed data.
Run with: python manage.py populate_db
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, time, timedelta
from authentication.models import CustomUser
from trainers.models import Trainer, SessionType, TrainerAvailability
from clients.models import ClientProfile
from bookings.models import Booking, Review
from gyms.models import City, Gym
import random

class Command(BaseCommand):
    help = 'Populate database with realistic seed data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n🚀 Starting database population...\n'))

        # 1. Create Cities
        self.stdout.write(self.style.WARNING('📍 Creating cities...'))
        cities_data = [
            ('casa', 'الدار البيضاء'),
            ('rabat', 'الرباط'),
            ('fez', 'فاس'),
            ('marrakech', 'مراكش'),
            ('agadir', 'أكادير'),
            ('tangier', 'طنجة'),
        ]
        
        cities = {}
        for code, name in cities_data:
            city, created = City.objects.get_or_create(
                code=code,
                defaults={'name': name}
            )
            cities[code] = city
            if created:
                self.stdout.write(f"  ✓ Created city: {name}")

        # 2. Create Session Types
        self.stdout.write(self.style.WARNING('\n💪 Creating session types...'))
        session_types_data = [
            ('تمارين اللياقة البدنية', 'fa-dumbbell'),
            ('اليوجا', 'fa-leaf'),
            ('الملاكمة', 'fa-fist-raised'),
            ('كروس فيت', 'fa-fire'),
            ('السباحة', 'fa-water'),
            ('التغذية', 'fa-apple-alt'),
            ('البيلاتس', 'fa-om'),
            ('الزومبا', 'fa-music'),
        ]
        
        session_types = {}
        for name, icon in session_types_data:
            st, created = SessionType.objects.get_or_create(
                name=name,
                defaults={'icon': icon}
            )
            session_types[name] = st
            if created:
                self.stdout.write(f"  ✓ Created session type: {name}")

        # 3. Create Trainers
        self.stdout.write(self.style.WARNING('\n👨‍🏫 Creating trainers...'))
        trainer_names = [
            ('محمد', 'علي'),
            ('أحمد', 'حسن'),
            ('علي', 'محمد'),
            ('فاطمة', 'خديجة'),
            ('سارة', 'مريم'),
            ('نور', 'زيد'),
            ('عماد', 'إبراهيم'),
            ('ليلى', 'نسيم'),
            ('كريم', 'طارق'),
            ('جنة', 'رجاء'),
        ]
        
        trainer_objs = []
        for first_name, last_name in trainer_names:
            # Create user
            username = f"trainer_{first_name.lower()}_{last_name.lower()}"
            user, created = CustomUser.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': f"{username}@fitnesmorocco.com",
                    'phone': f"+212{random.randint(600000000, 699999999)}",
                    'user_type': 'trainer',
                    'city': list(cities.values())[random.randint(0, len(cities)-1)].name,
                    'bio': f'مدرب محترف متخصص في اللياقة البدنية مع خبرة عملية كبيرة',
                }
            )
            if created:
                user.set_password('trainer123')
                user.save()

            # Create trainer profile
            trainer, created = Trainer.objects.get_or_create(
                user=user,
                defaults={
                    'experience_years': random.randint(2, 15),
                    'price_per_hour': random.choice([150, 200, 250, 300, 350, 400]),
                    'bio': f'أنا {first_name} {last_name}، مدرب شخصي معتمد متخصص في بناء الأجسام واللياقة البدنية. لديّ خبرة أكثر من {random.randint(2, 15)} سنوات في التدريب.',
                    'is_approved': True,
                    'rating': round(random.uniform(4.0, 5.0), 1),
                    'total_reviews': random.randint(5, 50),
                    'total_sessions': random.randint(50, 500),
                }
            )
            
            if created:
                # Add specialties
                selected_types = random.sample(list(session_types.values()), k=random.randint(2, 4))
                trainer.specialties.set(selected_types)
                trainer.save()
                self.stdout.write(f"  ✓ Created trainer: {first_name} {last_name}")
            
            trainer_objs.append(trainer)

        # 4. Create Trainer Availability
        self.stdout.write(self.style.WARNING('\n📅 Creating trainer availability...'))
        days = ['0', '1', '2', '3', '4']  # Monday to Friday
        for trainer in trainer_objs:
            for day in random.sample(days, k=random.randint(3, 5)):
                avail, created = TrainerAvailability.objects.get_or_create(
                    trainer=trainer,
                    day_of_week=day,
                    defaults={
                        'start_time': time(8, 0),
                        'end_time': time(20, 0),
                    }
                )
                if created:
                    self.stdout.write(f"  ✓ Added availability for {trainer.user.get_full_name()}")

        # 5. Create Clients
        self.stdout.write(self.style.WARNING('\n👥 Creating clients...'))
        client_names = [
            ('أحمد', 'محمود'),
            ('فاطمة', 'علي'),
            ('محمد', 'عمر'),
            ('سارة', 'حسن'),
            ('خالد', 'إبراهيم'),
            ('مريم', 'عبدالله'),
            ('علي', 'محمود'),
            ('نور', 'خالد'),
            ('رجاء', 'طارق'),
            ('أمير', 'سعيد'),
            ('ليلى', 'محمد'),
            ('زيد', 'عمر'),
            ('جنة', 'حسن'),
            ('عمرو', 'إبراهيم'),
            ('هناء', 'عبدالله'),
        ]
        
        client_objs = []
        for first_name, last_name in client_names:
            username = f"client_{first_name.lower()}_{last_name.lower()}"
            user, created = CustomUser.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': f"{username}@example.com",
                    'phone': f"+212{random.randint(600000000, 699999999)}",
                    'user_type': 'client',
                    'city': list(cities.values())[random.randint(0, len(cities)-1)].name,
                    'bio': 'مهتم باللياقة البدنية وتحسين صحتي',
                }
            )
            if created:
                user.set_password('client123')
                user.save()

            # Create client profile
            client_profile, created = ClientProfile.objects.get_or_create(
                user=user,
                defaults={
                    'fitness_level': random.choice(['beginner', 'intermediate', 'advanced']),
                    'age': random.randint(18, 60),
                    'gender': random.choice(['M', 'F']),
                    'weight': random.uniform(60, 100),
                    'height': random.uniform(160, 190),
                    'goals': 'تحسين لياقتي البدنية والحفاظ على صحتي',
                }
            )
            if created:
                self.stdout.write(f"  ✓ Created client: {first_name} {last_name}")
            
            client_objs.append(user)

        # 6. Create Bookings and Reviews
        self.stdout.write(self.style.WARNING('\n📅 Creating bookings and reviews...'))
        booking_count = 0
        for _ in range(40):
            client = random.choice(client_objs)
            trainer = random.choice(trainer_objs)
            
            # Create booking in the past (so we can add reviews)
            days_ago = random.randint(1, 60)
            booking_date_val = (timezone.now() - timedelta(days=days_ago)).date()
            
            try:
                booking = Booking.objects.create(
                    client=client,
                    trainer=trainer,
                    session_type=random.choice(list(session_types.values())),
                    booking_date=booking_date_val,
                    start_time=f"{random.randint(8, 20):02d}:{random.choice([0, 30]):02d}",
                    duration_minutes=random.choice([30, 60, 90, 120]),
                    status='completed',
                    total_price=trainer.price_per_hour,
                    notes=f'جلسة تدريبية مع {trainer.user.get_full_name()}',
                )
                
                booking_count += 1
                self.stdout.write(f"  ✓ Created booking #{booking_count}")
                
                # Add review if booking is completed
                if booking.status == 'completed':
                    review, rev_created = Review.objects.get_or_create(
                        booking=booking,
                        defaults={
                            'rating': random.randint(4, 5),
                            'comment': random.choice([
                                'جلسة رائعة جداً، المدرب احترافي وودود',
                                'استفدت كثيراً، سأحجز مرة أخرى بكل تأكيد',
                                'تجربة رائعة، المدرب ساعدني على تحقيق أهدافي',
                                'مدرب متميز وملهم، أنصح به بشدة',
                                'جودة عالية جداً، سعر مناسب وخدمة ممتازة',
                            ]),
                            'trainer': trainer,
                        }
                    )
                    if rev_created:
                        self.stdout.write(f"    ✓ Added review for booking")
            except Exception as e:
                # Skip duplicate bookings (same trainer, date, time)
                pass

        # 7. Create Gyms
        self.stdout.write(self.style.WARNING('\n🏋️ Creating gyms...'))
        
        # First create admin user for gym owner
        admin_user, _ = CustomUser.objects.get_or_create(
            username='gym_admin',
            defaults={
                'email': 'admin@gyms.com',
                'user_type': 'admin',
                'first_name': 'مدير',
                'last_name': 'الأندية',
            }
        )
        if _:
            admin_user.set_password('admin123')
            admin_user.save()
        
        gym_names = [
            'نادي اللياقة البدنية',
            'اكاديمية المحاربين',
            'صالة التدريب المتقدمة',
            'نادي الصحة والعافية',
            'اكاديمية البناء',
        ]
        
        for name in gym_names:
            try:
                gym, created = Gym.objects.get_or_create(
                    name=name,
                    defaults={
                        'owner': admin_user,
                        'city': list(cities.values())[random.randint(0, len(cities)-1)],
                        'address': f'شارع {random.choice(["النيل", "الملك فيصل", "محمد الخامس"])}، {name}',
                        'phone': f"+212{random.randint(500000000, 599999999)}",
                        'email': f"{name.replace(' ', '_')}@gym.com",
                        'description': f'نادي رياضي متخصص في {name}',
                        'rating': round(random.uniform(4.0, 5.0), 1),
                        'is_verified': True,
                    }
                )
                if created:
                    self.stdout.write(f"  ✓ Created gym: {name}")
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  ✗ Error creating gym {name}: {str(e)}"))

        self.stdout.write(self.style.SUCCESS('\n✅ Database population completed successfully!\n'))
        self.stdout.write(self.style.SUCCESS(f'Summary:'))
        self.stdout.write(f'  • Cities: {len(cities)}')
        self.stdout.write(f'  • Session Types: {len(session_types)}')
        self.stdout.write(f'  • Trainers: {len(trainer_objs)}')
        self.stdout.write(f'  • Clients: {len(client_objs)}')
        self.stdout.write(f'  • Bookings: {booking_count}')
        self.stdout.write(f'  • Gyms: {len(gym_names)}')
        self.stdout.write(self.style.SUCCESS('\n🎉 You can now login with:'))
        self.stdout.write('  • Trainer: trainer_محمد_علي / trainer123')
        self.stdout.write('  • Client: client_أحمد_محمود / client123')
