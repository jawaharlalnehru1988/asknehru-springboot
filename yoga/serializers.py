from rest_framework import serializers

from .models import PranayamaArticle, PranayamaSequence, YogaPose, YogaSequence


class YogaPoseSerializer(serializers.ModelSerializer):
	yogaName = serializers.CharField(source="yoga_name")
	blogContent = serializers.SerializerMethodField()
	audioURL = serializers.SerializerMethodField()
	imageURL = serializers.SerializerMethodField()
	videoURL = serializers.SerializerMethodField()

	class Meta:
		model = YogaPose
		fields = ["audioURL", "blogContent", "category", "id", "imageURL", "videoURL", "yogaName"]

	def _null_if_blank(self, value):
		if value is None:
			return None
		if isinstance(value, str) and value.strip() == "":
			return None
		return value

	def get_blogContent(self, obj):
		return self._null_if_blank(obj.blog_content)

	def get_audioURL(self, obj):
		return self._null_if_blank(obj.audio_url)

	def get_imageURL(self, obj):
		return self._null_if_blank(obj.image_url)

	def get_videoURL(self, obj):
		return self._null_if_blank(obj.video_url)


class YogaSequenceSerializer(serializers.ModelSerializer):
	sequenceName = serializers.CharField(source="sequence_name")
	blogContent = serializers.SerializerMethodField()
	audioURL = serializers.SerializerMethodField()
	imageURL = serializers.SerializerMethodField()
	videoURL = serializers.SerializerMethodField()

	class Meta:
		model = YogaSequence
		fields = ["audioURL", "blogContent", "category", "id", "imageURL", "sequenceName", "videoURL"]

	def _null_if_blank(self, value):
		if value is None:
			return None
		if isinstance(value, str) and value.strip() == "":
			return None
		return value

	def get_blogContent(self, obj):
		return self._null_if_blank(obj.blog_content)

	def get_audioURL(self, obj):
		return self._null_if_blank(obj.audio_url)

	def get_imageURL(self, obj):
		return self._null_if_blank(obj.image_url)

	def get_videoURL(self, obj):
		return self._null_if_blank(obj.video_url)


class PranayamaArticleSerializer(serializers.ModelSerializer):
	class Meta:
		model = PranayamaArticle
		fields = ["id", "pranayama_sequence", "title", "content", "category"]


class PranayamaSequenceSerializer(serializers.ModelSerializer):
	audioURL = serializers.CharField(source="audio_url", required=False, allow_blank=True, allow_null=True)
	relatedArticles = PranayamaArticleSerializer(source="articles", many=True, read_only=True)

	class Meta:
		model = PranayamaSequence
		fields = [
			"id",
			"name",
			"description",
			"steps",
			"duration",
			"benefits",
			"contraindications",
			"audioURL",
			"category",
			"relatedArticles",
		]

__all__ = [
	"PranayamaArticleSerializer",
	"PranayamaSequenceSerializer",
	"YogaPoseSerializer",
	"YogaSequenceSerializer",
]
