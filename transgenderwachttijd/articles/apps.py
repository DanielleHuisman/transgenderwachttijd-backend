import sys

from django.db import connection
from django.apps import AppConfig


class ArticlesConfig(AppConfig):
    name = 'transgenderwachttijd.articles'

    def ready(self):
        if sys.argv[-1] != 'migrate' and 'django_q_schedule' in connection.introspection.table_names():
            from .tasks import initialize_tasks
            initialize_tasks()
