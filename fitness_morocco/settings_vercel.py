import os
from pathlib import Path
from dotenv import load_dotenv

# PyMySQL as MySQLdb substitute
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

# Load environment variables
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# Security Settings for Production
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-1!u2n@y!7j81%#$)4)0^g_fb5y@(ihd1pldots%h+2o(z32frm')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Trust X-Forwarded-For header for Vercel
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = not DEBUG

# CSRF and security
CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', '').split(',') if os.getenv('CSRF_TRUSTED_ORIGINS') else []
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
SECURE_BROWSER_XSS_FILTER = True

# Minimal Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Local apps
    'core.apps.CoreConfig',
    'authentication.apps.AuthenticationConfig',
    'trainers.apps.TrainersConfig',
    'clients.apps.ClientsConfig',
    'bookings.apps.BookingsConfig',
    'dashboard.apps.DashboardConfig',
    'gyms.apps.GymsConfig',
    'payments.apps.PaymentsConfig',
]

# Optimized middleware (minimal for Vercel)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF = 'fitness_morocco.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'fitness_morocco.wsgi.application'

# Optimized Database Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'u386073008_fitness_morocc'),
        'USER': os.getenv('DB_USER', 'u386073008_fitness_admin'),
        'PASSWORD': os.getenv('DB_PASSWORD', '?M5Jh2NWSi'),
        'HOST': os.getenv('DB_HOST', 'auth-db1815.hstgr.io'),
        'PORT': os.getenv('DB_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
        'CONN_MAX_AGE': 300,  # Reduced for serverless
        'AUTOCOMMIT': True,
    }
}

# Authentication
AUTH_USER_MODEL = 'authentication.CustomUser'
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

# Minimal Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
]

# Internationalization
LANGUAGE_CODE = 'ar'
TIME_ZONE = 'Africa/Casablanca'
USE_I18N = True
USE_TZ = True

# Optimized Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
# Only include directories that exist to avoid warnings on Vercel
try:
    static_dir = BASE_DIR / 'static'
    STATICFILES_DIRS = [static_dir] if static_dir.exists() and static_dir.is_dir() else []
except Exception:
    STATICFILES_DIRS = []

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Only use FileSystemFinder if directories exist, otherwise just use AppDirectoriesFinder
if STATICFILES_DIRS:
    STATICFILES_FINDERS = [
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    ]
else:
    # On Vercel, just use app directories
    STATICFILES_FINDERS = [
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    ]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Minimal Logging (reduced for memory)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'level': 'WARNING',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}

# Cache configuration (minimal)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'fitness-cache',
        'OPTIONS': {
            'MAX_ENTRIES': 100
        }
    }
}

# Session configuration
SESSION_COOKIE_AGE = 1209600  # 2 weeks
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# Security
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_SECURITY_POLICY = {
    "default-src": ("'self'",),
    "script-src": ("'self'", "cdn.tailwindcss.com", "cdnjs.cloudflare.com"),
    "style-src": ("'self'", "'unsafe-inline'", "cdn.tailwindcss.com", "cdnjs.cloudflare.com"),
}

