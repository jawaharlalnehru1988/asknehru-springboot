from rest_framework import serializers

from .models import Roadmap


class RoadmapWriteSerializer(serializers.Serializer):
	mainTopic = serializers.CharField(max_length=200, required=False, trim_whitespace=True)
	syllabus = serializers.CharField(required=False, allow_blank=True, allow_null=True)
	routerLink = serializers.CharField(required=False, allow_blank=True, allow_null=True)
	intro = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)

	def validate(self, attrs):
		if not self.partial and not attrs.get("mainTopic"):
			raise serializers.ValidationError({"mainTopic": ["This field is required."]})

		for key in ["mainTopic", "routerLink", "intro"]:
			if key in attrs and attrs[key] is not None:
				attrs[key] = attrs[key].strip()
		return attrs


class RoadmapResponseSerializer(serializers.ModelSerializer):
	mainTopic = serializers.CharField(source="main_topic")
	imageUrl = serializers.SerializerMethodField()
	routerLink = serializers.CharField(source="router_link", allow_null=True)
	createdAt = serializers.DateTimeField(source="created_at", allow_null=True)
	updatedAt = serializers.DateTimeField(source="updated_at", allow_null=True)

	class Meta:
		model = Roadmap
		fields = [
			"id",
			"mainTopic",
			"syllabus",
			"imageUrl",
			"routerLink",
			"intro",
			"createdAt",
			"updatedAt",
		]

	def get_imageUrl(self, obj):
		if not obj.image_url:
			return None
		return f"/api/roadmaps/images/{obj.image_url}"


__all__ = ["RoadmapResponseSerializer", "RoadmapWriteSerializer"]
