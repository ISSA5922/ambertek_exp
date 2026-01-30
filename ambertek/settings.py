"""
Django settings for ambertek project.
"""

import os
import dj_database_url
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ambertek-export-dubai-tanzania-2024-secret-key'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# Application definition
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
    'accounts',  # ADD THIS - Authentication app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # For language support
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cart.middleware.CartAccessMiddleware',  
]

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
                # Add custom context processor for cart count
                'cart.context_processors.cart_items_count',
            ],
        },
    },
]

WSGI_APPLICATION = 'ambertek.wsgi.application'

# PostgreSQL Configuration for ambertek_export database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ambertek_export',      # Your database name in pgAdmin
        'USER': 'postgres',              # Default PostgreSQL username
        'PASSWORD': 'Ambertek',     # Your PostgreSQL password
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
DATABASES['default']=dj_database_url.parse("postgresql://postgess:9pw2Jgd61QDSjLkZgvyTUKPjr2SMBEZH@dpg-d5lrhjcoud1c738v15r0-a.oregon-postgres.render.com/ambertek_export")

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Supported languages
LANGUAGES = [
    ('en', 'English'),
    ('sw', 'Swahili'),
]

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files (Uploaded images, videos)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =============================================
# AUTHENTICATION & SESSION SETTINGS
# =============================================

# Authentication backends
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# Login/Logout URLs
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'  # Redirect to home after login
LOGOUT_REDIRECT_URL = '/'  # Redirect to home after logout

# Session settings
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 1209600  # 2 weeks in seconds (1209600)
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # Keep session alive after browser close
SESSION_SAVE_EVERY_REQUEST = True  # Save session on every request

# CSRF protection
CSRF_COOKIE_SECURE = False  # Set to True in production with HTTPS
CSRF_COOKIE_HTTPONLY = True
CSRF_USE_SESSIONS = False

# Security settings for development (change in production)
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# =============================================
# EMAIL CONFIGURATION - SECURITY WARNING!
# =============================================

# WARNING: Remove your actual password before committing to GitHub!
# Use environment variables in production

# For development, you can use console backend to test
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# REAL GMAIL CONFIGURATION
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = 'issaambari09@gmail.com'  # Your Gmail address
EMAIL_HOST_PASSWORD = 'dced pkgb nrqi gvyj'  # REMOVE THIS BEFORE SHARING CODE!
DEFAULT_FROM_EMAIL = 'Ambertek Exports <issaambari09@gmail.com>'
SERVER_EMAIL = 'issaambari09@gmail.com'

# Email settings for your business
ORDER_NOTIFICATION_EMAIL = 'issaambari09@gmail.com'  # Where admin notifications go
SUPPORT_EMAIL = 'support@ambertek.com'  # Customer support email (can be different)
ADMIN_EMAIL = 'issaambari09@gmail.com'  # Admin email

# Admin users who receive error emails
ADMINS = [
    ('Ambertek Admin', 'issaambari09@gmail.com'),
]

# Managers (receive broken link notifications)
MANAGERS = ADMINS

# =============================================
# LOGGING CONFIGURATION (for debugging)
# =============================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs/ambertek.log',
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file', 'mail_admins'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'ERROR',
        },
        'django.security': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'orders': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'accounts': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'utils': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# Create logs directory if it doesn't exist
log_dir = BASE_DIR / 'logs'
log_dir.mkdir(exist_ok=True)

# =============================================
# CUSTOM SETTINGS
# =============================================

# Site URL for email templates
SITE_URL = 'http://localhost:8000' if DEBUG else 'https://ambertek.com'

# Cart session key
CART_SESSION_ID = 'cart'

# Authentication requirements
MIN_PASSWORD_LENGTH = 8
MAX_LOGIN_ATTEMPTS = 5