"""
Django settings for ambertek project.
"""

import os
from pathlib import Path
import dj_database_url

# ==================================================
# BASE DIR
# ==================================================
BASE_DIR = Path(__file__).resolve().parent.parent

# ==================================================
# SECURITY
# ==================================================
SECRET_KEY = os.environ.get("SECRET_KEY", "unsafe-secret-key")

DEBUG = os.environ.get("DEBUG", "False").lower() == "true"

ALLOWED_HOSTS = os.environ.get(
    "ALLOWED_HOSTS",
    "localhost 127.0.0.1"
).split(" ")

# ==================================================
# APPLICATIONS
# ==================================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Custom apps
    'products',
    'orders',
    'cart',
    'home',
    'accounts',
]

# ==================================================
# MIDDLEWARE
# ==================================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cart.middleware.CartAccessMiddleware',
]

# ==================================================
# URLS & TEMPLATES
# ==================================================
ROOT_URLCONF = 'ambertek.urls'

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
                'cart.context_processors.cart_items_count',
            ],
        },
    },
]

WSGI_APPLICATION = 'ambertek.wsgi.application'

# ==================================================
# DATABASE (EXTERNAL POSTGRESQL)
# ==================================================
DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise Exception("DATABASE_URL environment variable not set")

DATABASES = {
    "default": dj_database_url.parse(
        DATABASE_URL,
        conn_max_age=600,
        ssl_require=True
    )
}

# ==================================================
# PASSWORD VALIDATION
# ==================================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8}
    },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ==================================================
# INTERNATIONALIZATION
# ==================================================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = [
    ('en', 'English'),
    ('sw', 'Swahili'),
]

# ==================================================
# STATIC & MEDIA FILES
# ==================================================
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ==================================================
# DEFAULT PRIMARY KEY
# ==================================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==================================================
# AUTH & SESSIONS
# ==================================================
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 1209600
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_SAVE_EVERY_REQUEST = True

# ==================================================
# SECURITY HEADERS
# ==================================================
CSRF_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_HTTPONLY = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# ==================================================
# EMAIL (USING ENV VARIABLES)
# ==================================================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")

DEFAULT_FROM_EMAIL = 'Ambertek Exports <issaambari09@gmail.com>'
SERVER_EMAIL = DEFAULT_FROM_EMAIL

SUPPORT_EMAIL = 'issaambari09@gmail.com'
ADMIN_EMAIL = 'issaambari09@gmail.com'

ADMINS = [('Ambertek Admin', ADMIN_EMAIL)]
MANAGERS = ADMINS

# ==================================================
# LOGGING
# ==================================================
LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

# ==================================================
# CUSTOM
# ==================================================
SITE_URL = 'http://localhost:8000' if DEBUG else 'https://ambertek.com'
CART_SESSION_ID = 'cart'
MIN_PASSWORD_LENGTH = 8
MAX_LOGIN_ATTEMPTS = 5
