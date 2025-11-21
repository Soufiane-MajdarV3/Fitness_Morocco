#!/bin/bash

# Fitness Morocco - Complete Setup Script
# This script will:
# 1. Update MySQL database settings
# 2. Run migrations
# 3. Populate the database
# 4. Create superuser

set -e

echo "🚀 Fitness Morocco - Complete Database Setup"
echo "=============================================="
echo ""

# Step 1: Ask for MySQL Host
read -p "📍 Enter your MySQL Host from Josted (e.g., mysql.josted.com): " MYSQL_HOST

if [ -z "$MYSQL_HOST" ]; then
    echo "❌ MySQL host is required!"
    exit 1
fi

echo "✅ MySQL Host: $MYSQL_HOST"
echo ""

# Step 2: Update settings.py
echo "🔧 Updating Django settings..."
cd /home/sofiane/Desktop/SaaS/Fitness

# Create a backup
cp fitness_morocco/settings.py fitness_morocco/settings.py.backup

# Update the HOST in settings.py
sed -i "s/'HOST': '127.0.0.1',/'HOST': '$MYSQL_HOST',/" fitness_morocc/settings.py

echo "✅ Settings updated"
echo ""

# Step 3: Test connection
echo "🧪 Testing database connection..."
python3 manage.py check

echo "✅ Database connection successful!"
echo ""

# Step 4: Run migrations
echo "📊 Running migrations..."
python3 manage.py migrate

echo "✅ Migrations completed!"
echo ""

# Step 5: Populate database
echo "📦 Populating database with seed data..."
python3 manage.py populate_db

echo "✅ Database populated!"
echo ""

# Step 6: Create admin user
echo "👤 Creating admin superuser..."
read -p "Enter admin username: " ADMIN_USER
read -sp "Enter admin password: " ADMIN_PASS
read -p "Enter admin email: " ADMIN_EMAIL
echo ""

# Create superuser programmatically
python3 manage.py shell << END
from authentication.models import CustomUser
if not CustomUser.objects.filter(username='$ADMIN_USER').exists():
    CustomUser.objects.create_superuser('$ADMIN_USER', '$ADMIN_EMAIL', '$ADMIN_PASS')
    print("✅ Superuser created successfully!")
else:
    print("⚠️ User already exists!")
END

echo ""
echo "✅ Setup completed successfully!"
echo ""
echo "🎉 Your platform is ready!"
echo ""
echo "📝 Quick Reference:"
echo "===================="
echo ""
echo "Start the server:"
echo "  python3 manage.py runserver"
echo ""
echo "Access the website:"
echo "  http://localhost:8000/"
echo ""
echo "Access admin panel:"
echo "  http://localhost:8000/admin/"
echo "  Username: $ADMIN_USER"
echo ""
echo "Test Accounts:"
echo "  Trainer: trainer_محمد_علي / trainer123"
echo "  Client: client_أحمد_محمود / client123"
echo ""
echo "Documentation:"
echo "  - README.md"
echo "  - MYSQL_SETUP_GUIDE.md"
echo "  - COMMANDS.md"
echo ""
