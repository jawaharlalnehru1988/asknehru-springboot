from rest_framework import serializers

from .models import Conversation
from core.serializer_utils import MAIN_TOPICS


class ConversationWriteSerializer(serializers.Serializer):
	mainTopic = serializers.CharField(max_length=100, required=False, trim_whitespace=True)
	subTopic = serializers.CharField(max_length=200, required=False, trim_whitespace=True)
	article = serializers.CharField(required=False, trim_whitespace=True)
	positiveConversation = serializers.CharField(required=False, allow_blank=True, allow_null=True)
	negativeConversation = serializers.CharField(required=False, allow_blank=True, allow_null=True)

	def validate(self, attrs):
		if not self.partial:
			required_fields = ["mainTopic", "subTopic", "article"]
			missing_fields = [field for field in required_fields if not attrs.get(field)]
			if missing_fields:
				raise serializers.ValidationError({field: ["This field is required."] for field in missing_fields})

		for key in ["mainTopic", "subTopic", "article"]:
			if key in attrs and attrs[key] is not None:
				attrs[key] = attrs[key].strip()
		for key in ["positiveConversation", "negativeConversation"]:
			if key in attrs and attrs[key] is not None:
				attrs[key] = attrs[key].strip()
		return attrs


class ConversationResponseSerializer(serializers.ModelSerializer):
	mainTopic = serializers.CharField(source="main_topic")
	subTopic = serializers.CharField(source="sub_topic")
	positiveConversation = serializers.CharField(source="positive_conversation", allow_null=True)
	negativeConversation = serializers.CharField(source="negative_conversation", allow_null=True)
	articleAudio = serializers.SerializerMethodField()
	conversationAudio = serializers.SerializerMethodField()
	createdAt = serializers.DateTimeField(source="created_at")
	updatedAt = serializers.DateTimeField(source="updated_at")

	class Meta:
		model = Conversation
		fields = [
			"id",
			"mainTopic",
			"subTopic",
			"article",
			"positiveConversation",
			"negativeConversation",
			"articleAudio",
			"conversationAudio",
			"createdAt",
			"updatedAt",
		]

	def get_articleAudio(self, obj):
		if not obj.article_audio:
			return None
		return f"/api/conversations/audio/{obj.article_audio}"

	def get_conversationAudio(self, obj):
		if not obj.conversation_audio:
			return None
		return f"/api/conversations/audio/{obj.conversation_audio}"


__all__ = ["ConversationResponseSerializer", "ConversationWriteSerializer", "MAIN_TOPICS"]
