from uuid import uuid4

from django.db import models


class Provider(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    name = models.CharField(max_length=255)
    website = models.URLField(max_length=255)
    scraped_at = models.DateTimeField(blank=True, null=True)


class Location(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)
    city = models.CharField(max_length=255)

    provider = models.ForeignKey(Provider, related_name='locations', on_delete=models.CASCADE)
