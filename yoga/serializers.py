from rest_framework import serializers

from .models import YogaPose


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


__all__ = ["YogaPoseSerializer"]
