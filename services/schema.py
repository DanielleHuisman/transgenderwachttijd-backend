import graphene
from graphene_django import DjangoObjectType

from . import models


class ServiceAgeGroup(DjangoObjectType):
    class Meta:
        model = models.ServiceAgeGroup


class ServiceType(DjangoObjectType):
    class Meta:
        model = models.ServiceType


class Service(DjangoObjectType):
    class Meta:
        model = models.Service


class ServiceOffering(DjangoObjectType):
    class Meta:
        model = models.ServiceOffering


class ServiceTime(DjangoObjectType):
    class Meta:
        model = models.ServiceTime


class Query(graphene.ObjectType):
    service_age_group = graphene.Field(ServiceAgeGroup, id=graphene.UUID())
    service_age_groups = graphene.NonNull(graphene.List(graphene.NonNull(ServiceAgeGroup)))

    service_type = graphene.Field(ServiceType, id=graphene.UUID())
    service_types = graphene.NonNull(graphene.List(graphene.NonNull(ServiceType)))

    def resolve_service_age_group(self, _info, **kwargs):
        return models.ServiceAgeGroup.objects.get(id=kwargs['id'])

    def resolve_service_age_groups(self, _info):
        return models.ServiceAgeGroup.objects.all()

    def resolve_service_type(self, _info, **kwargs):
        return models.ServiceType.objects.get(id=kwargs['id'])

    def resolve_service_types(self, _info):
        return models.ServiceType.objects.all()

    def resolve_service(self, _info, **kwargs):
        return models.Service.objects.get(id=kwargs['id'])

    def resolve_services(self, _info):
        return models.Service.objects.all()

    def resolve_service_offering(self, _info, **kwargs):
        return models.ServiceOffering.objects.get(id=kwargs['id'])

    def resolve_service_offerings(self, _info):
        return models.ServiceOffering.objects.all()

    def resolve_service_time(self, _info, **kwargs):
        return models.ServiceTime.objects.get(id=kwargs['id'])

    def resolve_service_times(self, _info):
        return models.ServiceTime.objects.all()
