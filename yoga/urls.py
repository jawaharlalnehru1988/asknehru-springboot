from django.urls import path

from .views import YogaPoseDetailView, YogaPosesSearchView, YogaPosesView


urlpatterns = [
    path("yoga/poses/search", YogaPosesSearchView.as_view()),
    path("yoga/poses", YogaPosesView.as_view()),
    path("yoga/poses/<int:pk>", YogaPoseDetailView.as_view()),
]
