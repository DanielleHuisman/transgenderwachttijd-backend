from typing import List

import strawberry

from .types import Provider, Location


@strawberry.type
class Query:
    provider: Provider = strawberry.django.field()
    providers: List[Provider] = strawberry.django.field()

    location: List[Location] = strawberry.django.field()
    locations: List[Location] = strawberry.django.field()
