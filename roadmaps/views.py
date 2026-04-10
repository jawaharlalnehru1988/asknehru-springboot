from django.conf import settings
from django.http import Http404
from django.utils import timezone
from rest_framework import status
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Roadmap
from core.serializer_utils import parse_json_part
from core.view_utils import delete_shared_file, ensure_directory, get_shared_file_response, save_uploaded_file

from .serializers import RoadmapResponseSerializer, RoadmapWriteSerializer


class RoadmapsView(APIView):
	parser_classes = [JSONParser, FormParser, MultiPartParser]

	def get(self, request):
		roadmaps = Roadmap.objects.order_by("-created_at", "-id")
		return Response(RoadmapResponseSerializer(roadmaps, many=True).data)

	def post(self, request):
		serializer = RoadmapWriteSerializer(data=parse_json_part(request.data.get("data")))
		serializer.is_valid(raise_exception=True)
		shared_dir = ensure_directory(settings.ASKNEHRU_SHARED_UPLOAD_DIR)
		image = request.FILES.get("image")
		roadmap = Roadmap.objects.create(
			main_topic=serializer.validated_data["mainTopic"],
			syllabus=serializer.validated_data.get("syllabus"),
			router_link=serializer.validated_data.get("routerLink"),
			intro=serializer.validated_data.get("intro"),
			image_url=save_uploaded_file(image, shared_dir) if image else None,
			created_at=timezone.now().replace(tzinfo=None),
			updated_at=timezone.now().replace(tzinfo=None),
		)
		return Response(RoadmapResponseSerializer(roadmap).data, status=status.HTTP_201_CREATED)


class RoadmapMainTopicsView(APIView):
	def get(self, request):
		topics = list(
			Roadmap.objects.order_by("-created_at", "-id").values_list("main_topic", flat=True)
		)
		return Response(topics)


class RoadmapDetailView(APIView):
	parser_classes = [JSONParser, FormParser, MultiPartParser]

	def get_object(self, pk: int) -> Roadmap:
		roadmap = Roadmap.objects.filter(pk=pk).first()
		if roadmap is None:
			raise Http404(f"Roadmap not found with id: {pk}")
		return roadmap

	def get(self, request, pk: int):
		return Response(RoadmapResponseSerializer(self.get_object(pk)).data)

	def put(self, request, pk: int):
		roadmap = self.get_object(pk)
		serializer = RoadmapWriteSerializer(data=parse_json_part(request.data.get("data")), partial=True)
		serializer.is_valid(raise_exception=True)
		data = serializer.validated_data
		shared_dir = ensure_directory(settings.ASKNEHRU_SHARED_UPLOAD_DIR)

		if "mainTopic" in data:
			roadmap.main_topic = data["mainTopic"]
		if "syllabus" in data:
			roadmap.syllabus = data["syllabus"]
		if "routerLink" in data:
			roadmap.router_link = data["routerLink"]
		if "intro" in data:
			roadmap.intro = data["intro"]

		image = request.FILES.get("image")
		if image:
			delete_shared_file(roadmap.image_url)
			roadmap.image_url = save_uploaded_file(image, shared_dir)

		roadmap.updated_at = timezone.now().replace(tzinfo=None)
		roadmap.save()
		return Response(RoadmapResponseSerializer(roadmap).data)

	def delete(self, request, pk: int):
		roadmap = self.get_object(pk)
		delete_shared_file(roadmap.image_url)
		roadmap.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)


class RoadmapImageView(APIView):
	def get(self, request, filename: str):
		return get_shared_file_response(filename)


__all__ = ["RoadmapDetailView", "RoadmapImageView", "RoadmapMainTopicsView", "RoadmapsView"]
