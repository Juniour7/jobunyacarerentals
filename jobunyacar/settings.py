from pathlib import Path
from dotenv import load_dotenv
import os
import logging

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!


# --- Security settings for production ---
DEBUG = False
SECURE_HSTS_SECONDS = 31536000  
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

SECURE_SSL_REDIRECT = True  

SESSION_COOKIE_SECURE = True  
CSRF_COOKIE_SECURE = True     

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"


# Settings For Local Development
# DEBUG = True
# SECURE_SSL_REDIRECT = False
# SESSION_COOKIE_SECURE = False
# CSRF_COOKIE_SECURE = False


ALLOWED_HOSTS = ['giftmacvane.pythonanywhere.com', '127.0.0.1', 'localhost']

AUTH_USER_MODEL = "rental_app.UserProfile"


# Application definition

INSTALLED_APPS = [
    'vehicles',
    'booking',
    'corsheaders',
    'rest_framework',
    'django_filters',
    'rest_framework.authtoken',
    'rental_app',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True
# or restrict to your frontend URL:
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:5173",  # React dev server
# ]


ROOT_URLCONF = 'jobunyacar.urls'

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

WSGI_APPLICATION = 'jobunyacar.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True



# ---------------------------------------------------------------------
# STATIC & MEDIA FILES
# ---------------------------------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # collectstatic will put all static here

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# use token auth by default (you can override per-view)
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 1000,
}

# For password reset email in dev:
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # prints emails to console
DEFAULT_FROM_EMAIL = 'webmaster@localhost'
# FRONTEND_URL used to build the password-reset link that you send to users:


ADMIN_EMAIL = 'giftmomanyi97@gmail.com'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.core.mail': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

# ----------------------------
# EMAIL SETTINGS (PRODUCTION)
# ----------------------------
# settings.py

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'mail.jobunyacarrentals.co.ke'  # from cPanel info
EMAIL_PORT = 465  # SSL port (recommended)
EMAIL_USE_SSL = True  # use SSL instead of TLS for port 465
EMAIL_USE_TLS = False

EMAIL_HOST_USER = 'no-reply@jobunyacarrentals.co.ke'
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')  # store safely in environment

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

FRONTEND_URL = 'https://jobunyacarrentals.co.ke/'  # your deployed frontend
