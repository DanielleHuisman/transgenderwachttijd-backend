from typing import List

import strawberry

from .types import ServiceAgeGroup, ServiceAgeGroupOrder, ServiceType, ServiceTypeOrder, Service, ServiceOrder, ServiceOffering, ServiceTime, ServiceTimeOrder


@strawberry.type
class Query:
    service_age_group: ServiceAgeGroup = strawberry.django.field()
    service_age_groups: List[ServiceAgeGroup] = strawberry.django.field(order=ServiceAgeGroupOrder)

    service_type: ServiceType = strawberry.django.field()
    service_types: List[ServiceType] = strawberry.django.field(order=ServiceTypeOrder)

    service: Service = strawberry.django.field()
    services: List[Service] = strawberry.django.field(order=ServiceOrder)

    service_offering: ServiceOffering = strawberry.django.field()
    service_offerings: List[ServiceOffering] = strawberry.django.field()

    service_time: ServiceTime = strawberry.django.field()
    service_times: List[ServiceTime] = strawberry.django.field(order=ServiceTimeOrder)
