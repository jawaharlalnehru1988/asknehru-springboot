from django.urls import path

from .views import UploadAudioView, UploadImageView


urlpatterns = [
    path("upload/image", UploadImageView.as_view()),
    path("upload/audio", UploadAudioView.as_view()),
]
