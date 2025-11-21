import os
import sys
from pathlib import Path

# Add project to path
sys.path.append(str(Path(__file__).resolve().parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitness_morocco.settings')

import django
django.setup()

from django.core.wsgi import get_wsgi_application
from django.conf import settings
from whitenoise import WhiteNoise

application = get_wsgi_application()

# Wrap with WhiteNoise for static file serving
if not settings.DEBUG:
    application = WhiteNoise(application, root=settings.STATIC_ROOT)
