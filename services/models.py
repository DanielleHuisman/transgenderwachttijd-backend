from uuid import uuid4

from django.db import models

from providers.models import Provider


class ServiceAgeGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class ServiceType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    name = models.CharField(max_length=255, unique=True)
    medical_name = models.CharField(max_length=255, unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank=True, null=True)
    dependencies = models.ManyToManyField('self', related_name='dependants', symmetrical=False, blank=True)

    def __str__(self):
        return self.name


class ServiceOffering(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    notes = models.TextField(blank=True, null=True)

    provider = models.ForeignKey(Provider, related_name='offerings', on_delete=models.CASCADE)
    service = models.ForeignKey(Service, related_name='offerings', on_delete=models.CASCADE)
    age_groups = models.ManyToManyField(ServiceAgeGroup, related_name='offerings', blank=True)
    types = models.ManyToManyField(ServiceType, related_name='offerings', blank=True)

    def __str__(self):
        service_name = self.service.medical_name if self.service.medical_name else self.service.name

        if self.age_groups.count() == ServiceAgeGroup.objects.count():
            age_groups = 'All groups'
        else:
            age_groups = ', '.join([str(age_group) for age_group in self.age_groups.all()])

        if self.types.count() == ServiceType.objects.count():
            types = 'All types'
        else:
            types = ', '.join([str(service_type) for service_type in self.types.all()])

        return f'{self.provider.name} - {service_name} ({age_groups} | {types})'


class ServiceTime(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    date = models.DateField(auto_now_add=True)
    days = models.PositiveIntegerField(blank=True, null=True)
    is_individual = models.BooleanField()
    has_stop = models.BooleanField()

    offering = models.ForeignKey(ServiceOffering, related_name='times', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.date.isoformat()} - {str(self.offering)}'
