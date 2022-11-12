from datetime import date
from typing import Optional

from strawberry import UNSET
from strawberry_django.ordering import apply as apply_order

from .models import Service, ServiceOffering, ServiceTime
from .types import GraphSeries, ServiceOrder


def resolve_graph(
        provider_ids: Optional[list[str]] = UNSET,
        service_ids: Optional[list[str]] = UNSET,
        service_age_group_ids: Optional[list[str]] = UNSET,
        service_type_ids: Optional[list[str]] = UNSET,
        start: Optional[date] = UNSET,
        end: Optional[date] = UNSET
) -> list[GraphSeries]:
    offerings_queryset = ServiceOffering.objects.order_by('provider__name', 'service__name')

    if provider_ids  != UNSET:
        offerings_queryset = offerings_queryset.filter(provider__id__in=provider_ids)
    if service_ids != UNSET:
        offerings_queryset = offerings_queryset.filter(service__id__in=service_ids)
    if service_age_group_ids != UNSET:
        offerings_queryset = offerings_queryset.filter(age_groups__id__in=service_age_group_ids)
    if service_type_ids != UNSET:
        offerings_queryset = offerings_queryset.filter(types__id__in=service_type_ids)

    series: list[GraphSeries] = []
    for offering in offerings_queryset:
        times_queryset = offering.times.order_by('date')

        if start != UNSET:
            times_queryset = times_queryset.filter(date__gte=start)
        if end != UNSET:
            times_queryset = times_queryset.filter(date__lte=end)

        series.append(GraphSeries(
            id=offering.id,
            label=str(offering),
            data=list(times_queryset)
        ))

    return series


def resolve_service_tree(order: Optional[ServiceOrder] = UNSET):
    queryset = Service.objects.filter(parent__isnull=True)

    queryset = apply_order(order, queryset)

    return queryset.all()
