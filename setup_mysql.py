#!/usr/bin/env python3
"""
Quick setup script for Fitness Morocco MySQL Database
Run: python3 setup_mysql.py
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, '/home/sofiane/Desktop/SaaS/Fitness')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitness_morocco.settings')

def setup_database():
    """Setup MySQL database with user input"""
    print("\n" + "="*60)
    print("🚀 FITNESS MOROCCO - MySQL Database Setup")
    print("="*60 + "\n")
    
    # Get MySQL host
    mysql_host = input("📍 Enter your MySQL Host from Josted\n   (e.g., mysql.josted.com or sql.josted.com):\n   > ").strip()
    
    if not mysql_host:
        print("❌ MySQL host is required!")
        return False
    
    mysql_port = input("\n🔌 Enter MySQL Port (default: 3306):\n   > ").strip() or "3306"
    
    print(f"\n✅ Configuration:")
    print(f"   Host: {mysql_host}")
    print(f"   Port: {mysql_port}")
    print(f"   Database: u386073008_fitness_morocc")
    print(f"   User: u386073008_fitness_admin")
    
    # Update settings file
    settings_path = '/home/sofiane/Desktop/SaaS/Fitness/fitness_morocco/settings.py'
    
    print(f"\n🔧 Updating settings.py...")
    
    with open(settings_path, 'r') as f:
        settings_content = f.read()
    
    # Replace HOST
    settings_content = settings_content.replace(
        "'HOST': '127.0.0.1',",
        f"'HOST': '{mysql_host}',"
    )
    
    # Replace PORT if not 3306
    settings_content = settings_content.replace(
        "'PORT': '3306',",
        f"'PORT': '{mysql_port}',"
    )
    
    with open(settings_path, 'w') as f:
        f.write(settings_content)
    
    print("✅ Settings updated!\n")
    
    # Test connection
    print("🧪 Testing database connection...")
    django.setup()
    
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✅ Database connection successful!\n")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("   Please check your MySQL host and credentials\n")
        return False
    
    # Ask to run migrations
    migrate_input = input("🔄 Run migrations now? (y/n) [y]: ").strip().lower() or "y"
    
    if migrate_input == "y":
        print("📊 Running migrations...")
        os.system("python3 /home/sofiane/Desktop/SaaS/Fitness/manage.py migrate")
        print("✅ Migrations completed!\n")
    
    # Ask to populate database
    populate_input = input("📦 Populate database with seed data? (y/n) [y]: ").strip().lower() or "y"
    
    if populate_input == "y":
        print("📦 Populating database...")
        os.system("python3 /home/sofiane/Desktop/SaaS/Fitness/manage.py populate_db")
        print("✅ Database populated!\n")
    
    # Ask to create superuser
    create_admin = input("👤 Create admin user? (y/n) [y]: ").strip().lower() or "y"
    
    if create_admin == "y":
        os.system("python3 /home/sofiane/Desktop/SaaS/Fitness/manage.py createsuperuser")
    
    print("\n" + "="*60)
    print("✅ Setup completed successfully!")
    print("="*60)
    print("\n🎉 Your Fitness Morocco platform is ready!\n")
    print("📝 Next Steps:")
    print("   1. Start the server:")
    print("      python3 manage.py runserver")
    print("")
    print("   2. Access the website:")
    print("      http://localhost:8000/")
    print("")
    print("   3. Access admin panel:")
    print("      http://localhost:8000/admin/")
    print("")
    print("   4. Test accounts:")
    print("      Trainer: trainer_محمد_علي / trainer123")
    print("      Client: client_أحمد_محمود / client123")
    print("\n")
    
    return True

if __name__ == "__main__":
    setup_database()
