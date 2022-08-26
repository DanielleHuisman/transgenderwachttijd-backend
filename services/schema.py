from typing import List

import strawberry

from .types import ServiceAgeGroup, ServiceType, Service


@strawberry.type
class Query:
    service_age_group: ServiceAgeGroup = strawberry.django.field()
    service_age_groups: List[ServiceAgeGroup] = strawberry.django.field()

    service_type: ServiceType = strawberry.django.field()
    service_types: List[ServiceType] = strawberry.django.field()
