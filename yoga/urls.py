from django.urls import path

from .views import (
    PranayamaArticleDetailView,
    PranayamaArticlesSearchView,
    PranayamaArticlesView,
    PranayamaSequenceDetailView,
    PranayamaSequencesSearchView,
    PranayamaSequencesView,
    YogaPoseDetailView,
    YogaPosesSearchView,
    YogaPosesView,
    YogaSequenceDetailView,
    YogaSequencesSearchView,
    YogaSequencesView,
)


urlpatterns = [
    path("yoga/poses/search", YogaPosesSearchView.as_view()),
    path("yoga/poses", YogaPosesView.as_view()),
    path("yoga/poses/<int:pk>", YogaPoseDetailView.as_view()),
    path("yoga/pranayama/sequences/search", PranayamaSequencesSearchView.as_view()),
    path("yoga/pranayama/sequences", PranayamaSequencesView.as_view()),
    path("yoga/pranayama/sequences/<int:pk>", PranayamaSequenceDetailView.as_view()),
    path("yoga/pranayama/articles/search", PranayamaArticlesSearchView.as_view()),
    path("yoga/pranayama/articles", PranayamaArticlesView.as_view()),
    path("yoga/pranayama/articles/<int:pk>", PranayamaArticleDetailView.as_view()),
    path("yoga/sequences/search", YogaSequencesSearchView.as_view()),
    path("yoga/sequences", YogaSequencesView.as_view()),
    path("yoga/sequences/<int:pk>", YogaSequenceDetailView.as_view()),
]
