
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================
# SECURITY
# ==============================

SECRET_KEY = os.getenv(
    'SECRET_KEY',
    'django-insecure-local-development-only'
)

DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

RENDER_EXTERNAL_HOSTNAME = os.getenv('RENDER_EXTERNAL_HOSTNAME')

if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

CSRF_TRUSTED_ORIGINS = [
    f'https://{RENDER_EXTERNAL_HOSTNAME}'
] if RENDER_EXTERNAL_HOSTNAME else []

# ==============================
# APPLICATIONS
# ==============================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'livres',
    'chatbot',
]

# ==============================
# MIDDLEWARE
# ==============================

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

ROOT_URLCONF = 'bibliotheque.urls'

# ==============================
# TEMPLATES
# ==============================

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'templates'],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ]
    },
}]

WSGI_APPLICATION = 'bibliotheque.wsgi.application'

# ==============================
# DATABASE
# SQLite - Demonstration
# ==============================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ==============================
# AUTHENTICATION
# ==============================

AUTH_PASSWORD_VALIDATORS = []

LOGIN_URL = '/auth/connexion/'
LOGIN_REDIRECT_URL = '/livres/'
LOGOUT_REDIRECT_URL = '/auth/connexion/'

# ==============================
# LANGUAGE AND TIME
# ==============================

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Tunis'
USE_I18N = True
USE_TZ = True

# ==============================
# STATIC FILES
# ==============================

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    [BASE_DIR / 'static']
    if (BASE_DIR / 'static').is_dir()
    else []
)

STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_STORAGE = (
    'whitenoise.storage.CompressedManifestStaticFilesStorage'
)

# ==============================
# MEDIA FILES
# ==============================

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ==============================
# DEFAULT PRIMARY KEY
# ==============================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==============================
# GEMINI AI CHATBOT
# ==============================

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
AI_PROVIDER = 'gemini'
