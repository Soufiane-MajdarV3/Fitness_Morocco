#!/bin/bash

# Pre-Deployment Checklist for Vercel

echo "🚀 Fitness Morocco - Pre-Deployment Checklist"
echo "=============================================="
echo ""

# Check Python version
echo "✓ Checking Python version..."
python3 --version

# Check requirements.txt
echo "✓ Checking requirements.txt..."
if [ -f "requirements.txt" ]; then
    echo "  Found: requirements.txt"
    echo "  Dependencies:"
    cat requirements.txt | grep -v "^#" | head -5
else
    echo "  ✗ requirements.txt not found!"
fi

echo ""

# Check critical files
echo "✓ Checking critical files..."
files=("vercel.json" "api/index.py" ".env.example" "fitness_morocco/settings_vercel.py" "build.sh")

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file"
    else
        echo "  ✗ $file (MISSING)"
    fi
done

echo ""

# Check Django setup
echo "✓ Checking Django setup..."
python3 manage.py check 2>/dev/null
if [ $? -eq 0 ]; then
    echo "  ✓ Django check passed"
else
    echo "  ✗ Django check failed"
fi

echo ""

# Check static files
echo "✓ Checking static files..."
python3 manage.py collectstatic --dry-run --noinput 2>/dev/null | tail -3

echo ""

# Check database migrations
echo "✓ Checking migrations..."
python3 manage.py showmigrations --plan 2>/dev/null | tail -5

echo ""

# Check Git setup
echo "✓ Checking Git repository..."
if [ -d ".git" ]; then
    echo "  ✓ Git repository initialized"
    echo "  Remote: $(git remote get-url origin 2>/dev/null || echo 'Not configured')"
else
    echo "  ✗ Git repository not initialized"
    echo "    Run: git init && git remote add origin <your-repo-url>"
fi

echo ""
echo "=============================================="
echo "✅ Pre-Deployment Checklist Complete!"
echo ""
echo "📋 Next Steps:"
echo "1. Review all ✗ items above"
echo "2. Push to GitHub: git push -u origin main"
echo "3. Go to https://vercel.com and import your repository"
echo "4. Add environment variables in Vercel dashboard"
echo "5. Click Deploy"
echo ""
echo "🔑 Remember to generate a new SECRET_KEY at https://djecrety.ir/"
