from typing import List

import strawberry

from .types import Provider, ProviderOrder, Location, LocationOrder


@strawberry.type
class Query:
    provider: Provider = strawberry.django.field()
    providers: List[Provider] = strawberry.django.field(order=ProviderOrder)

    location: List[Location] = strawberry.django.field()
    locations: List[Location] = strawberry.django.field(order=LocationOrder)
