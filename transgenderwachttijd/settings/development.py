# noinspection PyUnresolvedReferences
from .base import *

# Security

DEBUG = True


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
