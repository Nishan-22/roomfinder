import os
from pathlib import Path
import dj_database_url
import cloudinary
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent

# Cloudinary credentials (required on Render for images to show)
# Support either three env vars or single CLOUDINARY_URL (e.g. cloudinary://API_KEY:API_SECRET@CLOUD_NAME)
_clou_url = os.environ.get('CLOUDINARY_URL')
if _clou_url and _clou_url.startswith('cloudinary://'):
    try:
        # format: cloudinary://api_key:api_secret@cloud_name
        _parts = _clou_url.replace('cloudinary://', '').split('@')
        _key_secret = _parts[0].split(':', 1)
        CLOUDINARY_API_KEY = _key_secret[0]
        CLOUDINARY_API_SECRET = _key_secret[1] if len(_key_secret) > 1 else ''
        CLOUDINARY_CLOUD_NAME = _parts[1] if len(_parts) > 1 else ''
    except Exception:
        CLOUDINARY_CLOUD_NAME = CLOUDINARY_API_KEY = CLOUDINARY_API_SECRET = None
else:
    CLOUDINARY_CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME')
    CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY')
    CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET')
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
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cloudinary_storage',
    'django.contrib.staticfiles',
    'cloudinary',

    'whitenoise.runserver_nostatic',

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
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ======================
# CLOUDINARY MEDIA STORAGE (images on Render)
# ======================
if USE_CLOUDINARY:
    CLOUDINARY_STORAGE = {
        'CLOUD_NAME': CLOUDINARY_CLOUD_NAME,
        'API_KEY': CLOUDINARY_API_KEY,
        'API_SECRET': CLOUDINARY_API_SECRET,
        'SECURE': True,
    }
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
else:
    # Local dev fallback when env vars not set
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