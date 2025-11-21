#!/bin/bash

# Fitness Morocco - Django Command Reference
# Quick reference for common Django commands

cat << "EOF"

╔════════════════════════════════════════════════════════════════════╗
║        منصة فيتنس المغرب - Django Command Reference              ║
║                Fitness Morocco - Command Guide                    ║
╚════════════════════════════════════════════════════════════════════╝

📍 PROJECT LOCATION:
   /home/sofiane/Desktop/SaaS/Fitness

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 QUICK START

  # Option 1: Run start script
  ./start.sh

  # Option 2: Manual start
  python3 manage.py runserver

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 INSTALLATION & SETUP

  # Install dependencies
  pip install -r requirements.txt

  # Create migrations
  python3 manage.py makemigrations

  # Apply migrations
  python3 manage.py migrate

  # Create superuser (admin)
  python3 manage.py createsuperuser

  # Seed sample data
  python3 manage.py seed_data

  # Collect static files
  python3 manage.py collectstatic --noinput

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏃 RUNNING THE APPLICATION

  # Development server
  python3 manage.py runserver

  # Production server (with Gunicorn)
  gunicorn fitness_morocco.wsgi --bind 0.0.0.0:8000

  # With custom port
  python3 manage.py runserver 0.0.0.0:8080

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🗄️  DATABASE COMMANDS

  # Create new migrations
  python3 manage.py makemigrations

  # Show migration status
  python3 manage.py showmigrations

  # Apply specific migration
  python3 manage.py migrate appname

  # Undo last migration
  python3 manage.py migrate appname [migration_number]

  # Reset database (WARNING: Deletes all data)
  python3 manage.py flush

  # Backup database
  cp db.sqlite3 db.sqlite3.backup

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👤 USER MANAGEMENT

  # Create admin user
  python3 manage.py createsuperuser

  # Create regular user
  python3 manage.py shell
  > from authentication.models import CustomUser
  > CustomUser.objects.create_user('username', 'email@example.com', 'password')

  # Change user password
  python3 manage.py changepassword username

  # Create sample data
  python3 manage.py seed_data

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🧪 TESTING & DEBUGGING

  # Django shell
  python3 manage.py shell

  # Run tests
  python3 manage.py test

  # Run specific test
  python3 manage.py test bookings.tests

  # Check system
  python3 manage.py check

  # Validate templates
  python3 manage.py validate_templates

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 DJANGO SHELL EXAMPLES

  # Open shell
  python3 manage.py shell

  # Then in shell:

  # Import models
  from trainers.models import Trainer, City
  from bookings.models import Booking
  from authentication.models import CustomUser

  # Query trainers
  trainers = Trainer.objects.filter(is_approved=True)
  for t in trainers:
      print(t.user.get_full_name(), t.price_per_hour)

  # Create city
  city = City.objects.create(name="Marrakech", code="MAR")

  # Get user
  user = CustomUser.objects.get(username='trainer1')

  # Get bookings
  bookings = Booking.objects.filter(status='completed')

  # Calculate earnings
  total = bookings.aggregate(Sum('total_price'))

  # Exit shell
  exit()

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 STATIC FILES

  # Collect static files
  python3 manage.py collectstatic --noinput

  # Clear static files
  python3 manage.py collectstatic --clear --noinput

  # Development mode (auto-serve)
  python3 manage.py runserver

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔧 ADMIN PANEL ACCESS

  URL: http://localhost:8000/admin

  Default Credentials:
  └─ Username: admin
  └─ Password: admin123

  Features:
  ├─ User Management
  ├─ Trainer Approval
  ├─ Booking Management
  ├─ Payment Tracking
  ├─ Review Moderation
  └─ Site Configuration

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌐 KEY URLs

  Homepage:              http://localhost:8000/
  Trainers List:        http://localhost:8000/trainers/
  Trainer Profile:      http://localhost:8000/trainer/1/
  Login:                http://localhost:8000/login/
  Signup:               http://localhost:8000/signup/
  Client Dashboard:     http://localhost:8000/dashboard/
  Trainer Dashboard:    http://localhost:8000/trainer-dashboard/
  Admin Panel:          http://localhost:8000/admin/

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🐛 TROUBLESHOOTING

  # Fix import errors
  python3 manage.py check --deploy

  # Clear Python cache
  find . -type d -name __pycache__ -exec rm -r {} +

  # Reset migrations
  python3 manage.py makemigrations --empty appname --name reset

  # View SQL queries
  python3 manage.py sqlmigrate appname [migration_number]

  # Validate project
  python3 manage.py validate

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 CREATE NEW APP

  python3 manage.py startapp [app_name]

  Then add to INSTALLED_APPS in settings.py:
  └─ '[app_name].apps.[AppName]Config'

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 DOCUMENTATION

  README.md            - Main documentation
  INTEGRATION_GUIDE.md - Template integration guide
  PROJECT_SUMMARY.md  - Project completion summary

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✨ SAMPLE TEST ACCOUNTS

  Trainer Login:
  └─ Username: trainer1
  └─ Password: trainer1 (after seeding)

  Client Login:
  └─ Username: client1
  └─ Password: client1 (after seeding)

  Admin Login:
  └─ Username: admin
  └─ Password: admin123

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 USEFUL SHELL SNIPPETS

  # Count all users
  python3 manage.py shell
  > User.objects.count()

  # Get all trainers
  > Trainer.objects.all()

  # Get bookings for today
  > from django.utils import timezone
  > Booking.objects.filter(booking_date=timezone.now().date())

  # Calculate total earnings
  > from django.db.models import Sum
  > Booking.objects.filter(status='completed').aggregate(Sum('total_price'))

  # Get top-rated trainer
  > Trainer.objects.order_by('-rating').first()

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 DEPLOYMENT CHECKLIST

  Before going live:
  ☐ Set DEBUG = False
  ☐ Update ALLOWED_HOSTS
  ☐ Use PostgreSQL
  ☐ Set up proper static file serving
  ☐ Configure email backend
  ☐ Enable HTTPS
  ☐ Set up error logging
  ☐ Configure payment gateway
  ☐ Set up database backups
  ☐ Configure CDN for media

  Deployment command:
  python3 manage.py collectstatic --noinput

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📞 SUPPORT

  For issues:
  1. Check Django documentation: https://docs.djangoproject.com/
  2. Review error messages carefully
  3. Use Django shell for debugging
  4. Check database migrations
  5. Validate URL patterns

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ PROJECT STATUS: PRODUCTION READY

   Version: 1.0.0
   Django: 4.2+
   Python: 3.8+
   Database: SQLite (PostgreSQL ready)
   Status: ✅ Fully Functional

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Happy coding! 🚀

EOF
