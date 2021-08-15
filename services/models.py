from uuid import uuid4

from django.db import models

from providers.models import Provider


class ServiceAgeGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    name = models.CharField(max_length=255, unique=True)


class ServiceType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    name = models.CharField(max_length=255, unique=True)


class Service(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    provider = models.ForeignKey(Provider, related_name='services', on_delete=models.CASCADE)
    parent = models.ForeignKey(Provider, related_name='children', on_delete=models.CASCADE, blank=True, null=True)
    dependencies = models.ManyToManyField('self', related_name='dependants', blank=True)
    age_groups = models.ManyToManyField(ServiceAgeGroup, related_name='services', blank=True)
    types = models.ManyToManyField(ServiceType, related_name='services', blank=True)


class ServiceTime(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    date = models.DateField(auto_now_add=True)
    days = models.PositiveIntegerField()

    service = models.ForeignKey(Service, related_name='times', on_delete=models.CASCADE)
