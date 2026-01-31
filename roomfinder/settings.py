import os
from pathlib import Path
import dj_database_url
import cloudinary
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent

# Cloudinary credentials (required on Render for images to show)
# Support either three env vars or single CLOUDINARY_URL (e.g. cloudinary://API_KEY:API_SECRET@CLOUD_NAME)
# Strip values so trailing/leading spaces from Render env don't break URLs
def _strip(s):
    return (s or '').strip() or None

_clou_url = _strip(os.environ.get('CLOUDINARY_URL'))
if _clou_url and _clou_url.startswith('cloudinary://'):
    try:
        # format: cloudinary://api_key:api_secret@cloud_name
        _parts = _clou_url.replace('cloudinary://', '').split('@')
        _key_secret = _parts[0].split(':', 1)
        CLOUDINARY_API_KEY = _strip(_key_secret[0])
        CLOUDINARY_API_SECRET = _strip(_key_secret[1]) if len(_key_secret) > 1 else None
        CLOUDINARY_CLOUD_NAME = _strip(_parts[1]) if len(_parts) > 1 else None
    except Exception:
        CLOUDINARY_CLOUD_NAME = CLOUDINARY_API_KEY = CLOUDINARY_API_SECRET = None
else:
    CLOUDINARY_CLOUD_NAME = _strip(os.environ.get('CLOUDINARY_CLOUD_NAME'))
    CLOUDINARY_API_KEY = _strip(os.environ.get('CLOUDINARY_API_KEY'))
    CLOUDINARY_API_SECRET = _strip(os.environ.get('CLOUDINARY_API_SECRET'))
USE_CLOUDINARY = all([CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET])

if os.environ.get('RENDER') and not USE_CLOUDINARY:
    raise ImproperlyConfigured(
        'On Render, set Environment Variables in Dashboard: '
        'CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET. '
        'Get them from https://cloudinary.com/console'
    )

if USE_CLOUDINARY:
    cloudinary.config(
        cloud_name=CLOUDINARY_CLOUD_NAME,
        api_key=CLOUDINARY_API_KEY,
        api_secret=CLOUDINARY_API_SECRET,
        secure=True,
    )

# ======================
# SECURITY
# ======================
SECRET_KEY = os.environ.get('SECRET_KEY', 'unsafe-secret-key')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = ['*']  # or your render domain

# ======================
# APPLICATIONS
# ======================
# cloudinary_storage must come BEFORE django.contrib.staticfiles (per django-cloudinary-storage docs)
INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary_storage',
    'cloudinary',

    # Your app
    'rooms',
]

# ======================
# MIDDLEWARE
# ======================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'roomfinder.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'roomfinder.wsgi.application'

# ======================
# DATABASE
# ======================
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600,
        ssl_require=bool(os.environ.get('RENDER'))
    )
}

# ======================
# PASSWORD VALIDATION
# ======================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ======================
# INTERNATIONALIZATION
# ======================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ======================
# STATIC FILES (WhiteNoise)
# ======================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Use Whitenoise's recommended storage for Render
# We use CompressedStaticFilesStorage to avoid manifest issues while still getting compression
STORAGES = {
    'default': {
        'BACKEND': 'cloudinary_storage.storage.MediaCloudinaryStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage',
    },
}

# This prevents build failure if some files (like admin icons) are missing
WHITENOISE_MANIFEST_STRICT = False

# Media settings
if USE_CLOUDINARY:
    CLOUDINARY_STORAGE = {
        'CLOUD_NAME': CLOUDINARY_CLOUD_NAME,
        'API_KEY': CLOUDINARY_API_KEY,
        'API_SECRET': CLOUDINARY_API_SECRET,
        'SECURE': True,
    }
else:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'


# ======================
# LOGIN / LOGOUT
# ======================
LOGIN_REDIRECT_URL = 'room_list'
LOGOUT_REDIRECT_URL = 'room_list'

# ======================
# SECURITY FOR RENDER
# ======================
CSRF_TRUSTED_ORIGINS = [
    "https://roomfinder.onrender.com",
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'