from typing import List, TYPE_CHECKING

import strawberry
from strawberry import auto

if TYPE_CHECKING:
    from services.types import ServiceOffering, ServiceOfferingFilter, ServiceOfferingOrder

from . import models


@strawberry.django.filters.filter(models.Provider, lookups=True)
class ProviderFilter:
    id: auto

    name: auto
    slug: auto
    website: auto
    scraped_at: auto

    locations: 'LocationFilter'
    offerings: strawberry.LazyType['ServiceOfferingFilter', 'services.types']


@strawberry.django.ordering.order(models.Provider)
class ProviderOrder:
    id: auto

    name: auto
    slug: auto
    website: auto
    scraped_at: auto

    locations: 'LocationOrder'
    offerings: strawberry.LazyType['ServiceOfferingOrder', 'services.types']


@strawberry.django.type(models.Provider, filters=ProviderFilter, order=ProviderOrder)
class Provider:
    id: auto

    name: auto
    slug: auto
    website: auto
    scraped_at: auto

    locations: List['Location']
    offerings: List[strawberry.LazyType['ServiceOffering', 'services.types']]


@strawberry.django.filters.filter(models.Location, lookups=True)
class LocationFilter:
    id: auto

    name: auto
    address: auto
    postal_code: auto
    city: auto

    provider: 'ProviderFilter'


@strawberry.django.ordering.order(models.Location)
class LocationOrder:
    id: auto

    name: auto
    address: auto
    postal_code: auto
    city: auto

    provider: 'ProviderOrder'


@strawberry.django.type(models.Location, filters=LocationFilter, order=LocationOrder)
class Location:
    id: auto

    name: auto
    address: auto
    postal_code: auto
    city: auto

    provider: 'Provider'
