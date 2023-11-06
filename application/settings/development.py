# noinspection PyUnresolvedReferences
from .base import *

# Security

DEBUG = True

SECRET_KEY = '5cw1)q4ww+ckr5wevw@wr2zymp57$k@4fy3*@h2%(l79bx5b9i'

ALLOWED_HOSTS = ['localhost']


# Cross-Origin Resource Sharing (CORS)

CORS_ALLOWED_ORIGINS = ['http://localhost:3000']


# Cross Site Request Forgery (CSRF)

CSRF_TRUSTED_ORIGINS = []
