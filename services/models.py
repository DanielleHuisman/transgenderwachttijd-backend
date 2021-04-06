from uuid import uuid4

from django.db import models


class Service(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
