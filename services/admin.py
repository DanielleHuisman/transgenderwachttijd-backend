from django.contrib.admin import register, ModelAdmin
from modeltranslation.admin import TranslationAdmin

from .models import ServiceAgeGroup, ServiceType, Service, ServiceOffering, ServiceTime


@register(ServiceAgeGroup)
class ServiceAgeGroupAdmin(TranslationAdmin):
    list_display = ['id', 'name']
    list_filter = []


@register(ServiceType)
class ServiceTypeAdmin(TranslationAdmin):
    list_display = ['id', 'name']
    list_filter = []


@register(Service)
class ServiceAdmin(TranslationAdmin):
    list_display = ['id', 'name', 'medical_name', 'description', 'parent']
    list_filter = ['parent']


@register(ServiceOffering)
class ServiceOfferingAdmin(TranslationAdmin):
    list_display = ['id', 'provider', 'service', 'age_groups_str', 'types_str']
    list_filter = ['provider', 'service', 'age_groups', 'types']

    def age_groups_str(self, offering: ServiceOffering):
        if offering.age_groups.count() == ServiceAgeGroup.objects.count():
            return 'All groups'
        return ', '.join([str(age_group) for age_group in offering.age_groups.all()])

    def types_str(self, offering: ServiceOffering):
        if offering.types.count() == ServiceType.objects.count():
            return 'All types'
        return ', '.join([str(service_type) for service_type in offering.types.all()])


@register(ServiceTime)
class ServiceTimeAdmin(ModelAdmin):
    list_display = ['id', 'offering', 'date', 'days', 'is_individual', 'has_stop']
    list_filter = ['offering', 'date', 'is_individual', 'has_stop']
