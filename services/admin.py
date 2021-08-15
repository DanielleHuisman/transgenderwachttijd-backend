from django.contrib.admin import register, ModelAdmin
from modeltranslation.admin import TranslationAdmin

from .models import ServiceAgeGroup, ServiceType, Service, ServiceTime


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
    list_display = ['id', 'provider', 'name', 'description', 'parent']
    list_filter = ['provider', 'parent', 'age_groups', 'types']


@register(ServiceTime)
class ServiceTimeAdmin(ModelAdmin):
    list_display = ['id', 'service', 'date', 'days']
    list_filter = ['service', 'date']
