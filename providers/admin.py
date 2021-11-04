from django.contrib.admin import register, ModelAdmin

from .models import Provider, Location


@register(Provider)
class ProviderAdmin(ModelAdmin):
    list_display = ['id', 'name', 'scraped_at']
    list_filter = ['scraped_at']


@register(Location)
class LocationAdmin(ModelAdmin):
    list_display = ['id', 'name', 'address', 'postal_code', 'city']
    list_filter = ['city', 'provider']