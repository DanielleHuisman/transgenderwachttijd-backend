from django.contrib.admin import register, ModelAdmin

from .models import Provider, Location


@register(Provider)
class ProviderAdmin(ModelAdmin):
    list_display = ['id', 'name',  'website', 'scraped_at']
    list_filter = ['scraped_at']
    ordering = ['name']


@register(Location)
class LocationAdmin(ModelAdmin):
    list_display = ['id', 'name', 'address', 'postal_code', 'city']
    list_filter = ['city', 'provider']
    ordering = ['provider__name', 'name']
