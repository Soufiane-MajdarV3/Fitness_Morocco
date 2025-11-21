"""
WSGI config for fitness_morocco project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Determine which settings module to use
env = os.getenv('ENVIRONMENT', 'development')
if env == 'production':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitness_morocco.settings_vercel')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitness_morocco.settings')

application = get_wsgi_application()
