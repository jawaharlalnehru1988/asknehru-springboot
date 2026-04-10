from django.conf import settings
from django.http import Http404
from django.utils import timezone
from rest_framework import status
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Conversation
from core.serializer_utils import MAIN_TOPICS, parse_json_part
from core.view_utils import delete_shared_file, ensure_directory, get_shared_file_response, save_uploaded_file

from .serializers import ConversationResponseSerializer, ConversationWriteSerializer


class ConversationsMainTopicsView(APIView):
    def get(self, request):
        return Response(MAIN_TOPICS)


class ConversationsView(APIView):
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def get(self, request):
        conversations = Conversation.objects.order_by("id")
        return Response(ConversationResponseSerializer(conversations, many=True).data)

    def post(self, request):
        data_serializer = ConversationWriteSerializer(data=parse_json_part(request.data.get("data")))
        data_serializer.is_valid(raise_exception=True)
        shared_dir = ensure_directory(settings.ASKNEHRU_SHARED_UPLOAD_DIR)
        article_audio = request.FILES.get("articleAudio")
        conversation_audio = request.FILES.get("conversationAudio")
        now = timezone.now()
        conversation = Conversation.objects.create(
            main_topic=data_serializer.validated_data["mainTopic"],
            sub_topic=data_serializer.validated_data["subTopic"],
            article=data_serializer.validated_data["article"],
            positive_conversation=data_serializer.validated_data.get("positiveConversation"),
            negative_conversation=data_serializer.validated_data.get("negativeConversation"),
            article_audio=save_uploaded_file(article_audio, shared_dir) if article_audio else None,
            conversation_audio=save_uploaded_file(conversation_audio, shared_dir) if conversation_audio else None,
            created_at=now,
            updated_at=now,
        )
        return Response(ConversationResponseSerializer(conversation).data, status=status.HTTP_201_CREATED)


class ConversationDetailView(APIView):
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def get_object(self, pk: int) -> Conversation:
        conversation = Conversation.objects.filter(pk=pk).first()
        if conversation is None:
            raise Http404("Conversation not found.")
        return conversation

    def get(self, request, pk: int):
        return Response(ConversationResponseSerializer(self.get_object(pk)).data)

    def put(self, request, pk: int):
        conversation = self.get_object(pk)
        serializer = ConversationWriteSerializer(data=parse_json_part(request.data.get("data")), partial=True)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        shared_dir = ensure_directory(settings.ASKNEHRU_SHARED_UPLOAD_DIR)

        if "mainTopic" in data:
            conversation.main_topic = data["mainTopic"]
        if "subTopic" in data:
            conversation.sub_topic = data["subTopic"]
        if "article" in data:
            conversation.article = data["article"]
        if "positiveConversation" in data:
            conversation.positive_conversation = data["positiveConversation"]
        if "negativeConversation" in data:
            conversation.negative_conversation = data["negativeConversation"]

        article_audio = request.FILES.get("articleAudio")
        if article_audio:
            delete_shared_file(conversation.article_audio)
            conversation.article_audio = save_uploaded_file(article_audio, shared_dir)

        conversation_audio = request.FILES.get("conversationAudio")
        if conversation_audio:
            delete_shared_file(conversation.conversation_audio)
            conversation.conversation_audio = save_uploaded_file(conversation_audio, shared_dir)

        conversation.updated_at = timezone.now()
        conversation.save()
        return Response(ConversationResponseSerializer(conversation).data)

    def delete(self, request, pk: int):
        conversation = self.get_object(pk)
        delete_shared_file(conversation.article_audio)
        delete_shared_file(conversation.conversation_audio)
        conversation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ConversationAudioView(APIView):
    def get(self, request, filename: str):
        return get_shared_file_response(filename)


__all__ = [
    "ConversationAudioView",
    "ConversationDetailView",
    "ConversationsMainTopicsView",
    "ConversationsView",
]
