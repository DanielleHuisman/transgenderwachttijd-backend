import sentry_sdk
from django.conf import settings
from sentry_sdk.integrations.django import DjangoIntegration


def initialize_sentry():
    if settings.SENTRY_DSN:
        sentry_sdk.init(
            dsn=settings.SENTRY_DSN,
            integrations=[DjangoIntegration()],
            send_default_pii=True
        )
