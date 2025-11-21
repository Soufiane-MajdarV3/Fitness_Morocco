#!/bin/bash

# Fitness Morocco - Vercel Size Optimization
# Removes unnecessary files to stay under 2048 MB limit

echo "🧹 Cleaning up unnecessary files for Vercel deployment..."
echo "==========================================================="
echo ""

# Function to safely remove files
remove_if_exists() {
    if [ -e "$1" ]; then
        rm -rf "$1"
        echo "✓ Removed: $1"
    fi
}

# Remove SQLite database (will use MySQL in production)
remove_if_exists "db.sqlite3"

# Remove cache directories
echo ""
echo "Removing cache directories..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null
find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null
find . -type d -name ".hypothesis" -exec rm -rf {} + 2>/dev/null
find . -type d -name ".tox" -exec rm -rf {} + 2>/dev/null
find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null
find . -type d -name ".eggs" -exec rm -rf {} + 2>/dev/null

# Remove Python compiled files
echo "Removing Python cache files..."
find . -type f -name "*.pyc" -delete
find . -type f -name "*.pyo" -delete
find . -type f -name "*.pyd" -delete
find . -type f -name ".py[cod]" -delete

# Remove unnecessary documentation (keep only essential)
echo ""
echo "Cleaning documentation..."
# Keep only essential docs, remove duplicates
remove_if_exists "TEMPLATES_CONVERSION_SUMMARY.md"
remove_if_exists "README_TEMPLATES_GUIDE.md"

# Remove unnecessary scripts
echo ""
echo "Cleaning scripts..."
remove_if_exists "setup_mysql.py"
remove_if_exists "setup_database.sh"

# Remove media files (will be served from cloud storage in production)
echo ""
echo "Checking media files..."
if [ -d "media" ] && [ "$(ls -A media)" ]; then
    echo "⚠️  media/ directory found - consider uploading to cloud storage (S3, Cloudinary)"
    echo "   You can safely remove large media files locally"
fi

# Remove static files (will be collected at deployment)
remove_if_exists "staticfiles"

# Summary
echo ""
echo "==========================================================="
echo "✅ Cleanup complete!"
echo ""
echo "📊 New size:"
du -sh . 2>/dev/null || echo "Unable to calculate"
echo ""
echo "💡 Tips to further reduce size:"
echo "   1. Keep large media files in cloud storage"
echo "   2. Don't commit compiled files or cache"
echo "   3. Remove unused dependencies from requirements.txt"
echo "   4. Consider removing old migration files"
echo ""
