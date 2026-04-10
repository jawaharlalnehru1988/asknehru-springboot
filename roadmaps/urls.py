from django.urls import path

from .views import RoadmapDetailView, RoadmapImageView, RoadmapMainTopicsView, RoadmapsView


urlpatterns = [
    path("roadmaps/main-topics", RoadmapMainTopicsView.as_view()),
    path("roadmaps/images/<str:filename>", RoadmapImageView.as_view()),
    path("roadmaps", RoadmapsView.as_view()),
    path("roadmaps/<int:pk>", RoadmapDetailView.as_view()),
]
