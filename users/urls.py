from django.urls import path

from .views import UserDetailView, UsersView


urlpatterns = [
    path("users", UsersView.as_view()),
    path("users/<int:pk>", UserDetailView.as_view()),
]
