#!/bin/bash

# Build script for Vercel

echo "Installing dependencies..."
pip install -r requirements.txt --no-cache-dir

echo "Running migrations..."
ENVIRONMENT=production python manage.py migrate --no-input

echo "Collecting static files..."
ENVIRONMENT=production python manage.py collectstatic --noinput --verbosity 2 2>&1 | grep -v "staticfiles.W004"

echo "✅ Build complete!"
