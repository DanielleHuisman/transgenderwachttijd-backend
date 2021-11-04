from modeltranslation.translator import register, TranslationOptions

from .models import ServiceAgeGroup, ServiceType, Service, ServiceOffering


@register(ServiceAgeGroup)
class ServiceAgeGroupTranslationOptions(TranslationOptions):
    fields = ('name', )


@register(ServiceType)
class ServiceTypeTranslationOptions(TranslationOptions):
    fields = ('name', )


@register(Service)
class ServiceTranslationOptions(TranslationOptions):
    fields = ('name', 'medical_name', 'description')


@register(ServiceOffering)
class ServiceOfferingTranslationOptions(TranslationOptions):
    fields = ('notes', )
