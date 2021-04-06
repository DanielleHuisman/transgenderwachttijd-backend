from django.contrib import admin

from .models import Provider, Location


class ProviderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'scraped_at']
    list_filter = ['scraped_at']


class LocationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'address', 'postal_code', 'city']
    list_filter = ['city', 'provider']


admin.site.register(Provider, ProviderAdmin)
admin.site.register(Location, LocationAdmin)
