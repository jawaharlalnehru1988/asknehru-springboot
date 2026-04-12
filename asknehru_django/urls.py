from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("auth.urls")),
    path("api/", include("users.urls")),
    path("api/", include("medicines.urls")),
    path("api/", include("conversations.urls")),
    path("api/", include("roadmaps.urls")),
    path("api/", include("yoga.urls")),
    path("api/", include("uploads.urls")),
    path("api/", include("planning.urls")),
    path("api/", include("fruits.urls")),
]