from django.db import connection
from django.apps import AppConfig


class ArticlesConfig(AppConfig):
    name = 'articles'

    def ready(self):
        if 'django_q_schedule' in connection.introspection.table_names():
            from .tasks import initialize_tasks
            initialize_tasks()
