from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from strawberry.django.views import GraphQLView

from transgenderwachttijd.schema import schema

urlpatterns = [
    path('graphql', csrf_exempt(GraphQLView.as_view(schema=schema)))
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls)
)

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
