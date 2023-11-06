import os

from django.core.asgi import get_asgi_application

from .sentry import initialize_sentry

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings.production')

application = get_asgi_application()

initialize_sentry()
