from typing import List
from uuid import UUID

import strawberry
from strawberry import auto

from transgenderwachttijd.providers.types import Provider, ProviderFilter, ProviderOrder

from . import models


@strawberry.django.filters.filter(models.ServiceAgeGroup, lookups=True)
class ServiceAgeGroupFilter:
    id: auto

    name: auto


@strawberry.django.ordering.order(models.ServiceAgeGroup)
class ServiceAgeGroupOrder:
    id: auto

    name: auto

    offerings: 'ServiceOfferingOrder'


@strawberry.django.type(models.ServiceAgeGroup, filters=ServiceAgeGroupFilter, order=ServiceAgeGroupOrder)
class ServiceAgeGroup:
    id: auto

    name: auto

    offerings: List['ServiceOffering']


@strawberry.django.filters.filter(models.ServiceType, lookups=True)
class ServiceTypeFilter:
    id: auto

    name: auto


@strawberry.django.ordering.order(models.ServiceType)
class ServiceTypeOrder:
    id: auto

    name: auto

    offerings: 'ServiceOfferingOrder'


@strawberry.django.type(models.ServiceType, filters=ServiceTypeFilter, order=ServiceTypeOrder)
class ServiceType:
    id: auto

    name: auto

    offerings: List['ServiceOffering']


@strawberry.django.filters.filter(models.Service, lookups=True)
class ServiceFilter:
    id: auto

    name: auto
    medical_name: auto
    description: auto


@strawberry.django.ordering.order(models.Service)
class ServiceOrder:
    id: auto

    name: auto
    medical_name: auto
    description: auto

    parent: 'ServiceOrder'
    dependants: 'ServiceOrder'
    offerings: 'ServiceOfferingOrder'


@strawberry.django.type(models.Service, filters=ServiceFilter, order=ServiceOrder)
class Service:
    id: auto

    name: auto
    medical_name: auto
    description: auto

    parent: 'Service'
    children: List['Service']
    dependants: List['Service']
    offerings: List['ServiceOffering']


@strawberry.django.filters.filter(models.ServiceOffering, lookups=True)
class ServiceOfferingFilter:
    id: auto

    notes: auto

    provider: 'ProviderFilter'


@strawberry.django.ordering.order(models.ServiceOffering)
class ServiceOfferingOrder:
    id: auto

    notes: auto

    provider: 'ProviderOrder'
    age_groups: 'ServiceAgeGroupOrder'
    types: 'ServiceTypeOrder'
    times: 'ServiceTimeOrder'


@strawberry.django.type(models.ServiceOffering, filters=ServiceOfferingFilter, order=ServiceOfferingOrder)
class ServiceOffering:
    id: auto

    notes: auto

    provider: 'Provider'
    service: 'Service'
    age_groups: List['ServiceAgeGroup']
    types: List['ServiceType']
    times: List['ServiceTime']


@strawberry.django.filters.filter(models.ServiceTime, lookups=True)
class ServiceTimeFilter:
    id: auto

    date: auto
    days: auto
    is_individual: auto
    has_stop: auto

    offering: 'ServiceOfferingFilter'


@strawberry.django.ordering.order(models.ServiceTime)
class ServiceTimeOrder:
    id: auto

    date: auto
    days: auto
    is_individual: auto
    has_stop: auto

    offering: 'ServiceOfferingOrder'


@strawberry.django.type(models.ServiceTime, filters=ServiceTimeFilter, order=ServiceTimeOrder)
class ServiceTime:
    id: auto

    date: auto
    days: auto
    is_individual: auto
    has_stop: auto

    offering: 'ServiceOffering'


@strawberry.type
class GraphSeries:
    id: UUID
    label: str
    data: list[ServiceTime]
