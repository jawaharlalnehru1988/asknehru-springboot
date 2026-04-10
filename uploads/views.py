from django.conf import settings
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from core.view_utils import build_upload_response, save_uploaded_file

from .serializers import UploadResponseSerializer


class UploadImageView(APIView):
	parser_classes = [FormParser, MultiPartParser]

	def post(self, request):
		uploaded_file = request.FILES.get("file")
		if not uploaded_file:
			return Response({"error": "Please select a file to upload"}, status=status.HTTP_400_BAD_REQUEST)
		content_type = uploaded_file.content_type or ""
		if not content_type.startswith("image/"):
			return Response({"error": "Only image files are allowed"}, status=status.HTTP_400_BAD_REQUEST)
		if uploaded_file.size > 5 * 1024 * 1024:
			return Response({"error": "File size must be less than 5MB"}, status=status.HTTP_400_BAD_REQUEST)

		filename = save_uploaded_file(uploaded_file, settings.ASKNEHRU_YOGA_IMAGE_UPLOAD_DIR)
		response = UploadResponseSerializer(build_upload_response(filename, "/media/yoga-poses/")).data
		return Response(response)


class UploadAudioView(APIView):
	parser_classes = [FormParser, MultiPartParser]

	def post(self, request):
		uploaded_file = request.FILES.get("file")
		if not uploaded_file:
			return Response({"error": "Please select a file to upload"}, status=status.HTTP_400_BAD_REQUEST)
		content_type = uploaded_file.content_type or ""
		if not content_type.startswith("audio/"):
			return Response({"error": "Only audio files are allowed"}, status=status.HTTP_400_BAD_REQUEST)
		if uploaded_file.size > 50 * 1024 * 1024:
			return Response({"error": "Audio size must be less than 50MB"}, status=status.HTTP_400_BAD_REQUEST)

		filename = save_uploaded_file(uploaded_file, settings.ASKNEHRU_YOGA_AUDIO_UPLOAD_DIR)
		response = UploadResponseSerializer(build_upload_response(filename, "/media/yoga-audio/")).data
		return Response(response)


__all__ = ["UploadAudioView", "UploadImageView"]
