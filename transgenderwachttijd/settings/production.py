from .base import *

# Security

DEBUG = parse_boolean(os.getenv('DEBUG'))

SECRET_KEY = os.getenv('SECRET_KEY')

ALLOWED_HOSTS = [origin.strip() for origin in os.getenv('ALLOWED_HOSTS', '').split(',')]

FORCE_SCRIPT_NAME = os.getenv('FORCE_SCRIPT_NAME')


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


# Cache

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache'
    }
}


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
