import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


def parse_boolean(value: Optional[str]):
    return value and value.strip().lower() == 'true'


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load environment variables
load_dotenv(os.path.join(BASE_DIR, '.env'))


# Security

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = parse_boolean(os.getenv('DEBUG'))

ALLOWED_HOSTS = [origin.strip() for origin in os.getenv('ALLOWED_HOSTS', '').split(',')]

FORCE_SCRIPT_NAME = os.getenv('FORCE_SCRIPT_NAME')


# Application definition

INSTALLED_APPS = [
    'modeltranslation',
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'django_q',
    'strawberry.django',
    'transgenderwachttijd.articles',
    'transgenderwachttijd.providers',
    'transgenderwachttijd.services'
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
    'django.middleware.locale.LocaleMiddleware'
]

ROOT_URLCONF = 'transgenderwachttijd.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'application.wsgi.application'

SITE_ID = 1


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': os.getenv('DATABASE_HOST', 'localhost'),
        'PORT': os.getenv('DATABASE_PORT', '3306'),
        'USER': os.getenv('DATABASE_USERNAME', 'transgenderwachttijd'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', ''),
        'NAME': os.getenv('DATABASE_NAME', 'transgenderwachttijd')
    }
}


# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Cache

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache'
    }
}


# Password validation

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

LANGUAGE_CODE = 'en'

TIME_ZONE = os.getenv('TIME_ZONE', 'Europe/Amsterdam')

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = [
    ('en', 'English'),
    ('nl', 'Nederlands')
]


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'dist', 'static')
STATICFILES_DIRS = []


# Media files (user uploads)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.getenv('MEDIA_ROOT', os.path.join(BASE_DIR, 'media'))


# Cross-Origin Resource Sharing (CORS)

CORS_ALLOWED_ORIGINS = [origin.strip() for origin in os.getenv('CORS_ALLOWED_ORIGINS', '').split(',')]

CORS_ALLOW_CREDENTIALS = False


# Cross Site Request Forgery (CSRF)

CSRF_COOKIE_DOMAIN = os.getenv('CSRF_COOKIE_DOMAIN')

CSRF_COOKIE_SECURE = True

CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in os.getenv('CSRF_TRUSTED_ORIGINS', '').split(',')]


# Session

SESSION_COOKIE_SAMESITE = 'Lax'

SESSION_COOKIE_SECURE = True


# Sentry

SENTRY_DSN = os.getenv('SENTRY_DSN')


# Django Q

Q_CLUSTER = {
    'name': 'DjangoORM',
    'workers': 2,
    'timeout': 90,
    'retry': 120,
    'bulk': 10,
    'orm': 'default',
    'error_reporter': {
        'sentry': {
            'dsn': SENTRY_DSN
        }
    } if SENTRY_DSN else None
}
