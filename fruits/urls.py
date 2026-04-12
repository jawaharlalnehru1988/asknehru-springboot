from django.urls import path

from .views import FruitGalleryDetailView, FruitsGalleryView


urlpatterns = [
    path("fruits-gallery", FruitsGalleryView.as_view()),
    path("fruits-gallery/<int:pk>", FruitGalleryDetailView.as_view()),
]
