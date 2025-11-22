from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from payments.models import SubscriptionPlan, Organization
from trainers.models import Trainer, SessionType
from bookings.models import Review
from decimal import Decimal
from datetime import datetime, timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Initialize database with real data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Starting database initialization...')
        
        # 1. Create subscription plans
        self.create_subscription_plans()
        
        # 2. Create test organizations/clubs
        self.create_organizations()
        
        # 3. Create trainers and reviews
        self.create_trainers_and_reviews()
        
        self.stdout.write(self.style.SUCCESS('✅ Database initialization complete!'))

    def create_subscription_plans(self):
        """Create the 4 subscription plans"""
        plans_data = [
            {
                'key': 'basic',
                'name': 'Basic',
                'description': 'Get started with fitness tracking',
                'price_monthly': Decimal('0.00'),
                'price_annual': Decimal('0.00'),
                'is_org_plan': False,
                'included_seats': 1,
                'commission_rate': Decimal('20.00'),
                'features': ['Create profile', 'Browse trainers', 'Limited bookings', 'Basic analytics']
            },
            {
                'key': 'premium',
                'name': 'Premium',
                'description': 'For active fitness enthusiasts',
                'price_monthly': Decimal('99.00'),
                'price_annual': Decimal('990.00'),
                'is_org_plan': False,
                'included_seats': 1,
                'commission_rate': Decimal('15.00'),
                'features': ['Unlimited bookings', 'Priority support', 'Advanced analytics', 'Trainer recommendations', 'Performance tracking']
            },
            {
                'key': 'club',
                'name': 'Club',
                'description': 'For growing fitness clubs',
                'price_monthly': Decimal('500.00'),
                'price_annual': Decimal('5000.00'),
                'is_org_plan': True,
                'included_seats': 10,
                'overage_price_per_seat': Decimal('40.00'),
                'commission_rate': Decimal('12.00'),
                'features': ['10 trainer seats', 'Member management', 'Booking analytics', 'Marketing tools', 'Staff dashboard', 'Commission tracking', '24/7 support']
            },
            {
                'key': 'gold_club',
                'name': 'Gold Club',
                'description': 'For premium fitness establishments',
                'price_monthly': Decimal('1200.00'),
                'price_annual': Decimal('12000.00'),
                'is_org_plan': True,
                'included_seats': 50,
                'overage_price_per_seat': Decimal('30.00'),
                'commission_rate': Decimal('12.00'),
                'features': ['50 trainer seats', 'Advanced member management', 'Real-time analytics', 'Custom branding', 'API access', 'Dedicated account manager', '24/7 priority support', 'Custom integrations']
            }
        ]
        
        for plan_data in plans_data:
            plan, created = SubscriptionPlan.objects.get_or_create(
                key=plan_data['key'],
                defaults=plan_data
            )
            if created:
                self.stdout.write(f'✅ Created plan: {plan.name}')
            else:
                self.stdout.write(f'⏭️  Plan already exists: {plan.name}')

    def create_organizations(self):
        """Create real fitness clubs/organizations"""
        clubs_data = [
            {
                'name': 'FitnessPro Casablanca',
                'email': 'contact@fitnesspro-casa.ma',
                'phone': '+212 5 22 12 34 56',
                'city': 'Casablanca',
                'address': 'Rue de la Corniche, Casablanca',
                'description': 'Center de fitness moderne avec équipements dernier cri, cours collectifs et entraînement personnalisé. Situé au cœur de Casablanca, nous offrons des programmes adaptés pour tous les niveaux.',
                'website': 'https://fitnesspro-casa.ma',
                'latitude': Decimal('33.5731'),
                'longitude': Decimal('-7.5898'),
            },
            {
                'name': 'Elite Gym Rabat',
                'email': 'info@elitegym-rabat.ma',
                'phone': '+212 5 37 68 90 12',
                'city': 'Rabat',
                'address': 'Avenue Bourguiba, Rabat',
                'description': 'Salle de sport haut de gamme avec piscine, spa et zone de relaxation. Spécialisée dans le fitness fonctionnel et le CrossFit. Coachs diplômés disponibles 7j/7.',
                'website': 'https://elitegym-rabat.ma',
                'latitude': Decimal('34.0209'),
                'longitude': Decimal('-6.8416'),
            },
            {
                'name': 'Power House Marrakech',
                'email': 'hello@powerhouse-mkc.ma',
                'phone': '+212 5 24 44 55 66',
                'city': 'Marrakech',
                'address': 'Boulevard de la Menara, Marrakech',
                'description': 'Complexe fitness complet avec studio yoga, salle de musculation et zone cardio. Ambiance chaleureuse et accueillante avec coachs expérimentés. Parking gratuit.',
                'website': 'https://powerhouse-mkc.ma',
                'latitude': Decimal('31.6295'),
                'longitude': Decimal('-8.0100'),
            },
            {
                'name': 'Flex Sports Fes',
                'email': 'contact@flexsports-fes.ma',
                'phone': '+212 5 35 62 34 56',
                'city': 'Fes',
                'address': 'Rue de la Liberté, Fes',
                'description': 'Salle de gym dynamique avec équipements modernes et coachs personnels. Cours de boxe, yoga et HIIT. Nutrition et conseil fitness inclus dans les memberships premium.',
                'website': 'https://flexsports-fes.ma',
                'latitude': Decimal('34.0331'),
                'longitude': Decimal('-5.0033'),
            },
            {
                'name': 'Summit Athletic Agadir',
                'email': 'info@summitathetic-agadir.ma',
                'phone': '+212 5 28 82 34 56',
                'city': 'Agadir',
                'address': 'Corniche d\'Agadir',
                'description': 'Club de fitness premium avec vue sur l\'océan. Entraînement personnalisé, cours collectifs et programmes de nutritionniste. Accès piscine et jacuzzi inclus.',
                'website': 'https://summitathetic.ma',
                'latitude': Decimal('30.4278'),
                'longitude': Decimal('-9.5982'),
            },
            {
                'name': 'Urban Fitness Tangier',
                'email': 'contact@urbanfitness-tng.ma',
                'phone': '+212 5 39 93 34 56',
                'city': 'Tangier',
                'address': 'Boulevard Pasteur, Tangier',
                'description': 'Studio de fitness urbain avec focus sur les tendances fitness actuelles. CrossFit, pilates et cours collectifs innovants. Coachs certifiés internationaux.',
                'website': 'https://urbanfitness.ma',
                'latitude': Decimal('35.7595'),
                'longitude': Decimal('-5.8116'),
            },
        ]
        
        for i, club_data in enumerate(clubs_data):
            # Create owner user for each club
            email = club_data['email']
            owner, _ = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': email.split('@')[0],
                    'first_name': club_data['name'].split()[0],
                    'last_name': ' '.join(club_data['name'].split()[1:]),
                    'user_type': 'owner'
                }
            )
            
            # Create organization
            plan = SubscriptionPlan.objects.get(key='club' if i < 3 else 'gold_club')
            org, created = Organization.objects.get_or_create(
                name=club_data['name'],
                defaults={
                    'owner': owner,
                    'subscription_plan': plan,
                    'email': club_data['email'],
                    'phone': club_data['phone'],
                    'city': club_data['city'],
                    'address': club_data['address'],
                    'description': club_data['description'],
                    'website': club_data['website'],
                    'latitude': club_data.get('latitude'),
                    'longitude': club_data.get('longitude'),
                    'is_active': True,
                    'is_verified': True,
                    'subscription_start': datetime.now(),
                    'subscription_end': datetime.now() + timedelta(days=365),
                }
            )
            
            if created:
                self.stdout.write(f'✅ Created club: {org.name}')
            else:
                self.stdout.write(f'⏭️  Club already exists: {org.name}')

    def create_trainers_and_reviews(self):
        """Create trainers with realistic reviews"""
        trainers_data = [
            {
                'name': 'Ahmed Hassan',
                'email': 'ahmed.hassan@trainers.ma',
                'specialty': 'Musculation',
                'bio': 'Coach de musculation avec 8 ans d\'expérience. Spécialisé dans la prise de masse et la définition musculaire. Certifié IFBB.',
                'price': Decimal('150.00'),
                'experience': 8,
                'reviews': [
                    {'rating': 5, 'text': 'Ahmed est un excellent coach! Très professionnel et motivant. J\'ai vu des résultats incroyables en 3 mois.'},
                    {'rating': 5, 'text': 'Meilleur coach que j\'ai jamais eu. Il adapte les programmes selon mes objectifs et mon niveau.'},
                    {'rating': 4, 'text': 'Très bon coach, très disponible et à l\'écoute. Je recommande vivement!'},
                ]
            },
            {
                'name': 'Fatima El Amrani',
                'email': 'fatima.amrani@trainers.ma',
                'specialty': 'Yoga & Pilates',
                'bio': 'Instructrice yoga certifiée avec passion pour le bien-être. 6 ans d\'expérience dans le yoga vinyasa et le yin yoga.',
                'price': Decimal('120.00'),
                'experience': 6,
                'reviews': [
                    {'rating': 5, 'text': 'Fatima a vraiment changé ma vie. Ses cours sont relaxants et très efficaces pour la flexibilité.'},
                    {'rating': 5, 'text': 'Super instructrice, très patiente et bienveillante. L\'ambiance lors des cours est magique.'},
                    {'rating': 5, 'text': 'J\'adore ses cours! Elle crée une atmosphère très zen et apaisante.'},
                ]
            },
            {
                'name': 'Mohamed Saidi',
                'email': 'mohamed.saidi@trainers.ma',
                'specialty': 'CrossFit & HIIT',
                'bio': 'Coach CrossFit certifié avec 7 ans d\'expérience en entraînement fonctionnel. Ancien athlète professionnel.',
                'price': Decimal('180.00'),
                'experience': 7,
                'reviews': [
                    {'rating': 5, 'text': 'Mohamed est un coach incroyable! Son énergie est contagieuse et les entraînements sont variés.'},
                    {'rating': 4, 'text': 'Très bon coach, très motivant. Les séances sont intenses mais accessibles à tous les niveaux.'},
                    {'rating': 5, 'text': 'Best coach ever! Il me pousse toujours au-delà de mes limites de façon positive.'},
                ]
            },
            {
                'name': 'Aida Bennani',
                'email': 'aida.bennani@trainers.ma',
                'specialty': 'Fitness & Cardio',
                'bio': 'Entraîneuse fitness dynamique avec 5 ans d\'expérience. Spécialisée dans les cours collectifs et le cardio.',
                'price': Decimal('100.00'),
                'experience': 5,
                'reviews': [
                    {'rating': 5, 'text': 'Aida est fantastique! Ses cours de cardio sont amusants et efficaces pour perdre du poids.'},
                    {'rating': 4, 'text': 'Bonne coach, très énergique et motivante. Ambiance super lors des séances en groupe.'},
                    {'rating': 5, 'text': 'J\'adore les cours d\'Aida! Elle crée une bonne ambiance et c\'est très motivant.'},
                ]
            },
            {
                'name': 'Karim Bennani',
                'email': 'karim.bennani@trainers.ma',
                'specialty': 'Entraînement Personnel',
                'bio': 'Coach personnel certifié avec 9 ans d\'expérience. Approche holistique combinant fitness, nutrition et mindfulness.',
                'price': Decimal('200.00'),
                'experience': 9,
                'reviews': [
                    {'rating': 5, 'text': 'Karim est un coach extraordinaire! Il comprend vos objectifs et crée un plan parfait pour vous.'},
                    {'rating': 5, 'text': 'Très professionnel et dédié. Karim m\'a aidé à atteindre des objectifs que je pensais impossibles.'},
                    {'rating': 5, 'text': 'Coach exceptionnel! Résultats garantis avec Karim. Je le recommande à 100%.'},
                ]
            },
            {
                'name': 'Leila Mansouri',
                'email': 'leila.mansouri@trainers.ma',
                'specialty': 'Danse & Zumba',
                'bio': 'Instructrice danse avec 4 ans d\'expérience en cours de zumba et danse fitness. Danseuse professionnel auparavant.',
                'price': Decimal('110.00'),
                'experience': 4,
                'reviews': [
                    {'rating': 5, 'text': 'Leila rend l\'entraînement amusant! Ses cours de zumba sont énergétiques et motivants.'},
                    {'rating': 5, 'text': 'Super instructrice! On ne voit pas le temps passer pendant ses cours. C\'est magique!'},
                    {'rating': 4, 'text': 'Très bon cours! Leila crée une bonne ambiance et les mouvements sont faciles à suivre.'},
                ]
            },
        ]
        
        for trainer_data in trainers_data:
            # Create or get user
            user, _ = User.objects.get_or_create(
                email=trainer_data['email'],
                defaults={
                    'username': trainer_data['email'].split('@')[0],
                    'first_name': trainer_data['name'].split()[0],
                    'last_name': ' '.join(trainer_data['name'].split()[1:]),
                    'user_type': 'trainer'
                }
            )
            
            # Create trainer
            trainer, created = Trainer.objects.get_or_create(
                user=user,
                defaults={
                    'bio': trainer_data['bio'],
                    'price_per_hour': trainer_data['price'],
                    'experience_years': trainer_data['experience'],
                    'is_approved': True
                }
            )
            
            if created:
                self.stdout.write(f'✅ Created trainer: {trainer_data["name"]}')
            else:
                self.stdout.write(f'⏭️  Trainer already exists: {trainer_data["name"]}')
            
            # Create reviews
            for review_data in trainer_data['reviews']:
                # Create a dummy client user for each review
                review_client_email = f'client_{trainer_data["email"].split(".")[0]}_{review_data["rating"]}@example.ma'
                review_user, _ = User.objects.get_or_create(
                    email=review_client_email,
                    defaults={
                        'username': review_client_email.split('@')[0],
                        'first_name': f'Client{review_data["rating"]}',
                        'last_name': trainer_data['name'].split()[-1],
                        'user_type': 'client'
                    }
                )
                
                Review.objects.get_or_create(
                    trainer=trainer,
                    client=review_user,
                    defaults={
                        'rating': review_data['rating'],
                        'comment': review_data['text'],
                        'created_at': datetime.now() - timedelta(days=30)
                    }
                )
            
            self.stdout.write(f'✅ Created {len(trainer_data["reviews"])} reviews for {trainer_data["name"]}')
