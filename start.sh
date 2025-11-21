#!/bin/bash

# Fitness Morocco - Quick Start Script
# This script sets up and runs the Django project

echo "🏋️ Fitness Morocco - Platform Setup"
echo "======================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Step 1: Check Python installation
echo -e "${YELLOW}Step 1: Checking Python installation...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 is not installed. Please install Python 3.8+${NC}"
    exit 1
fi
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}✓ Python ${PYTHON_VERSION} found${NC}"
echo ""

# Step 2: Navigate to project directory
echo -e "${YELLOW}Step 2: Setting up project directory...${NC}"
cd "$(dirname "$0")"
echo -e "${GREEN}✓ Working directory: $(pwd)${NC}"
echo ""

# Step 3: Create virtual environment (if not exists)
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Step 3: Creating virtual environment...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
fi
echo ""

# Step 4: Activate virtual environment
echo -e "${YELLOW}Step 4: Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"
echo ""

# Step 5: Install dependencies
echo -e "${YELLOW}Step 5: Installing dependencies...${NC}"
pip install -r requirements.txt > /dev/null 2>&1
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Step 6: Run migrations
echo -e "${YELLOW}Step 6: Applying database migrations...${NC}"
python3 manage.py migrate > /dev/null 2>&1
echo -e "${GREEN}✓ Database migrations applied${NC}"
echo ""

# Step 7: Check if superuser exists
echo -e "${YELLOW}Step 7: Checking admin account...${NC}"
python3 manage.py shell << END > /dev/null 2>&1
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    print("CREATE_ADMIN")
END

if grep -q "CREATE_ADMIN" <<< "$(python3 manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    print('CREATE_ADMIN')
END
)"; then
    echo -e "${YELLOW}Creating admin account (admin/admin123)...${NC}"
    python3 manage.py shell << END > /dev/null 2>&1
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@fitness.local', 'admin123')
    print("Admin created")
END
    echo -e "${GREEN}✓ Admin account created (username: admin, password: admin123)${NC}"
else
    echo -e "${GREEN}✓ Admin account already exists${NC}"
fi
echo ""

# Step 8: Seed data
echo -e "${YELLOW}Step 8: Seeding initial data...${NC}"
python3 manage.py seed_data > /dev/null 2>&1
echo -e "${GREEN}✓ Sample data created (5 trainers, 20 clients, etc.)${NC}"
echo ""

# Step 9: Run development server
echo -e "${GREEN}======================================"
echo "✓ Setup completed successfully!"
echo "=====================================${NC}"
echo ""
echo -e "${YELLOW}Starting development server...${NC}"
echo ""
echo "📱 Access the application:"
echo "   Homepage: http://localhost:8000"
echo "   Admin: http://localhost:8000/admin"
echo ""
echo "👤 Admin Credentials:"
echo "   Username: admin"
echo "   Password: admin123"
echo ""
echo "🔍 Sample Accounts:"
echo "   Trainer: trainer1 / trainer1"
echo "   Client: client1 / client1"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
echo ""

python3 manage.py runserver
