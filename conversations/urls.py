from django.urls import path

from .views import ConversationAudioView, ConversationDetailView, ConversationsMainTopicsView, ConversationsView


urlpatterns = [
    path("conversations/main-topics", ConversationsMainTopicsView.as_view()),
    path("conversations/audio/<str:filename>", ConversationAudioView.as_view()),
    path("conversations", ConversationsView.as_view()),
    path("conversations/<int:pk>", ConversationDetailView.as_view()),
]
