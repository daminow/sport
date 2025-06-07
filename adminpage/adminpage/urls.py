# adminpage/urls.py
"""adminpage URL Configuration"""

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from sport.admin.site import site

# Normalize URL prefix: Django `path()` patterns must not start with a slash
prefix = getattr(settings, "PREFIX", "").lstrip("/")

handler404 = "sport.views.errors.handler404"
handler500 = "sport.views.errors.handler500"

urlpatterns = [
    # Если в settings.PREFIX передан префикс, Django обработает его,
    # иначе просто пустая строка → корень.
    path(prefix, include([
        path("", include("sport.urls")),
        path("", include("django_prometheus.urls")),
        path("admin/", site.urls),
        path("oauth2/", include("django_auth_adfs.urls")),
        path("api/", include("api.urls")),
        path("media/", include("media.urls")),
        path("hijack/", include("hijack.urls")),
    ])),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)