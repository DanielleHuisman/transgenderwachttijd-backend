from typing import Optional

import strawberry
from strawberry_django.ordering import apply as apply_order

from .models import Service
from .types import ServiceOrder


def resolve_service_tree(order: Optional[ServiceOrder] = strawberry.UNSET):
    queryset = Service.objects.filter(parent__isnull=True)

    queryset = apply_order(order, queryset)

    return queryset.all()
