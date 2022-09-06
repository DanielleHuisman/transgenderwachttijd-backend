from typing import List, TYPE_CHECKING

import strawberry
from strawberry import auto

from providers.types import Provider

from . import models


@strawberry.django.type(models.ServiceAgeGroup)
class ServiceAgeGroup:
    id: auto

    name: auto

    offerings: List['ServiceOffering']


@strawberry.django.ordering.order(models.ServiceAgeGroup)
class ServiceAgeGroupOrder:
    name: auto


@strawberry.django.type(models.ServiceType)
class ServiceType:
    id: auto

    name: auto

    offerings: List['ServiceOffering']


@strawberry.django.ordering.order(models.ServiceType)
class ServiceTypeOrder:
    name: auto


@strawberry.django.type(models.Service)
class Service:
    id: auto

    name: auto
    medical_name: auto
    description: auto

    parent: 'Service'
    dependants: List['Service']
    offerings: List['ServiceOffering']


@strawberry.django.ordering.order(models.Service)
class ServiceOrder:
    name: auto
    medical_name: auto


@strawberry.django.type(models.ServiceOffering)
class ServiceOffering:
    id: auto

    notes: auto

    provider: 'Provider'
    service: 'Service'
    age_groups: List['ServiceAgeGroup']
    types: List['ServiceType']
    times: List['ServiceTime']


@strawberry.django.type(models.ServiceTime)
class ServiceTime:
    id: auto

    date: auto
    days: auto
    is_individual: auto
    has_stop: auto

    offering: 'ServiceOffering'


@strawberry.django.ordering.order(models.ServiceTime)
class ServiceTimeOrder:
    date: auto
