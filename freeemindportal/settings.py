"""
Django settings for freeemindportal project.
"""

from pathlib import Path
import os
import dj_database_url


# =========================================================
# BASE DIRECTORY
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# =========================================================
# SECURITY
# =========================================================

SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-development-only-key'
)

DEBUG = os.environ.get(
    'DEBUG',
    'False'
).lower() == 'true'


# =========================================================
# ALLOWED HOSTS
# =========================================================

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'freemind-auction-portal1.onrender.com',
]

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

ONLINE_HOST = os.environ.get('ONLINE_HOST')
if ONLINE_HOST and ONLINE_HOST not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(ONLINE_HOST)


# =========================================================
# CSRF TRUSTED ORIGINS
# =========================================================

CSRF_TRUSTED_ORIGINS = [
    'http://localhost',
    'http://127.0.0.1',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'https://freemind-auction-portal1.onrender.com',
    'https://*.onrender.com',
]

if RENDER_EXTERNAL_HOSTNAME:
    CSRF_TRUSTED_ORIGINS.append(f'https://{RENDER_EXTERNAL_HOSTNAME}')

ONLINE_URL = os.environ.get('ONLINE_URL')
if ONLINE_URL and ONLINE_URL not in CSRF_TRUSTED_ORIGINS:
    CSRF_TRUSTED_ORIGINS.append(ONLINE_URL)


# =========================================================
# APPLICATIONS
# =========================================================

INSTALLED_APPS = [

    'jazzmin',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Cloudinary Apps
    'cloudinary_storage',
    'cloudinary',

    'auctions',
]


# =========================================================
# MIDDLEWARE
# =========================================================

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


# =========================================================
# URL CONFIGURATION
# =========================================================

ROOT_URLCONF = 'freeemindportal.urls'


# =========================================================
# TEMPLATES
# =========================================================

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


# =========================================================
# WSGI
# =========================================================

WSGI_APPLICATION = 'freeemindportal.wsgi.application'


# =========================================================
# DATABASE
# =========================================================

DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            ssl_require=True,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# =========================================================
# PASSWORD VALIDATION
# =========================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# =========================================================
# INTERNATIONALIZATION
# =========================================================

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Dar_es_Salaam'

USE_I18N = True

USE_TZ = True


# =========================================================
# STATIC FILES
# =========================================================

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# =========================================================
# MEDIA FILES
# =========================================================

MEDIA_URL = '/media/'

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
}


# =========================================================
# LOGIN / LOGOUT
# =========================================================

LOGIN_URL = '/accounts/login/'

LOGIN_REDIRECT_URL = '/dashboard-redirect/'

LOGOUT_REDIRECT_URL = '/'


# =========================================================
# EMAIL - GMAIL SMTP
# =========================================================

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'

EMAIL_PORT = 587

EMAIL_USE_TLS = True

EMAIL_HOST_USER = os.environ.get(
    'EMAIL_HOST_USER',
    ''
)

EMAIL_HOST_PASSWORD = os.environ.get(
    'EMAIL_HOST_PASSWORD',
    ''
)

DEFAULT_FROM_EMAIL = os.environ.get(
    'DEFAULT_FROM_EMAIL',
    'Freemind Auction Agency <freemindagency2023@gmail.com>'
)


# =========================================================
# PRODUCTION SECURITY
# =========================================================

if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = (
        'HTTP_X_FORWARDED_PROTO',
        'https'
    )


# =========================================================
# JAZZMIN SETTINGS
# =========================================================

JAZZMIN_SETTINGS = {
    "site_title": "Freemind Auction Admin",
    "site_header": "Freemind Auction",
    "site_brand": "Freemind Portal",
    "welcome_sign": "Karibu kwenye Freemind Auction Admin Portal",
    "copyright": "Freemind Agency",
}


# =========================================================
# DEFAULT PRIMARY KEY
# =========================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'