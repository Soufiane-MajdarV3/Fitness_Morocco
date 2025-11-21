import os
import sys
from pathlib import Path

# Add project to path
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Set production environment for Vercel
os.environ.setdefault('ENVIRONMENT', 'production')
os.environ.setdefault('DEBUG', 'False')

# Use Vercel settings if in production
if os.environ.get('ENVIRONMENT') == 'production':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitness_morocco.settings_vercel')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitness_morocco.settings')

import django
django.setup()

from django.core.wsgi import get_wsgi_application
from django.conf import settings
from whitenoise import WhiteNoise

application = get_wsgi_application()

# Wrap with WhiteNoise for static file serving
staticfiles_dir = getattr(settings, 'STATIC_ROOT', None)
if staticfiles_dir and os.path.exists(staticfiles_dir):
    application = WhiteNoise(application, root=staticfiles_dir)

# Export app variable for Vercel
app = application
