from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from places.views import start, place_detail

urlpatterns = [
    path("", start, name="start"),
    path("places/<int:pk>/", place_detail, name="place_detail"),
    path("admin/", admin.site.urls),
    path("tinymce/", include("tinymce.urls")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
