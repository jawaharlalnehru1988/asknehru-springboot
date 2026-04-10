from django.conf import settings
from django.http import Http404
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import YogaPose
from core.view_utils import delete_managed_media, delete_replaced_media

from .serializers import YogaPoseSerializer


class YogaPosesView(APIView):
	parser_classes = [JSONParser]

	def get(self, request):
		poses = YogaPose.objects.order_by("id")
		return Response(YogaPoseSerializer(poses, many=True).data)

	def post(self, request):
		serializer = YogaPoseSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		pose = YogaPose.objects.create(**serializer.validated_data)
		return Response(YogaPoseSerializer(pose).data, status=status.HTTP_201_CREATED)


class YogaPoseDetailView(APIView):
	parser_classes = [JSONParser]

	def get_object(self, pk: int) -> YogaPose:
		pose = YogaPose.objects.filter(pk=pk).first()
		if pose is None:
			raise Http404(f"Yoga pose not found with id: {pk}")
		return pose

	def get(self, request, pk: int):
		return Response(YogaPoseSerializer(self.get_object(pk)).data)

	def put(self, request, pk: int):
		pose = self.get_object(pk)
		serializer = YogaPoseSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		updated = serializer.validated_data

		delete_replaced_media(
			pose.audio_url,
			updated.get("audio_url"),
			settings.ASKNEHRU_YOGA_AUDIO_UPLOAD_DIR,
			"/media/yoga-audio/",
		)
		delete_replaced_media(
			pose.image_url,
			updated.get("image_url"),
			settings.ASKNEHRU_YOGA_IMAGE_UPLOAD_DIR,
			"/media/yoga-poses/",
		)
		delete_replaced_media(
			pose.video_url,
			updated.get("video_url"),
			settings.ASKNEHRU_YOGA_VIDEO_UPLOAD_DIR,
			"/media/yoga-video/",
		)

		pose.yoga_name = updated["yoga_name"]
		pose.blog_content = updated.get("blog_content")
		pose.audio_url = updated.get("audio_url")
		pose.video_url = updated.get("video_url")
		pose.image_url = updated.get("image_url")
		pose.category = updated.get("category")
		pose.save()
		return Response(YogaPoseSerializer(pose).data)

	def delete(self, request, pk: int):
		pose = self.get_object(pk)
		delete_managed_media(pose.audio_url, settings.ASKNEHRU_YOGA_AUDIO_UPLOAD_DIR, "/media/yoga-audio/")
		delete_managed_media(pose.image_url, settings.ASKNEHRU_YOGA_IMAGE_UPLOAD_DIR, "/media/yoga-poses/")
		delete_managed_media(pose.video_url, settings.ASKNEHRU_YOGA_VIDEO_UPLOAD_DIR, "/media/yoga-video/")
		pose.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)


class YogaPosesSearchView(APIView):
	def get(self, request):
		yoga_name = request.query_params.get("yogaName", "")
		poses = YogaPose.objects.filter(yoga_name__icontains=yoga_name).order_by("id")
		return Response(YogaPoseSerializer(poses, many=True).data)


__all__ = ["YogaPoseDetailView", "YogaPosesSearchView", "YogaPosesView"]
