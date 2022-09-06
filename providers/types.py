from typing import List, TYPE_CHECKING

import strawberry
from strawberry import auto

if TYPE_CHECKING:
    from services.types import ServiceOffering

from . import models


@strawberry.django.type(models.Provider)
class Provider:
    id: auto

    name: auto
    slug: auto
    website: auto
    scraped_at: auto

    locations: List['Location']
    offerings: List[strawberry.LazyType['ServiceOffering', 'services.types']]


@strawberry.django.ordering.order(models.Provider)
class ProviderOrder:
    name: auto
    slug: auto
    scraped_at: auto


@strawberry.django.type(models.Location)
class Location:
    id: auto

    name: auto
    address: auto
    postal_code: auto
    city: auto

    provider: 'Provider'


@strawberry.django.ordering.order(models.Location)
class LocationOrder:
    name: auto
    city: auto
