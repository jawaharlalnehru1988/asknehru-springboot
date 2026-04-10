from django.conf import settings
from django.http import Http404
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import PranayamaArticle, PranayamaSequence, YogaPose, YogaSequence
from core.view_utils import delete_managed_media, delete_replaced_media

from .serializers import (
	PranayamaArticleSerializer,
	PranayamaSequenceSerializer,
	YogaPoseSerializer,
	YogaSequenceSerializer,
)


class YogaPosesView(APIView):
	parser_classes = [JSONParser]

	def get(self, request):
		poses = YogaPose.objects.exclude(category="sequence")
		category = request.query_params.get("category")
		if category:
			poses = poses.filter(category__iexact=category)
		poses = poses.order_by("id")
		return Response(YogaPoseSerializer(poses, many=True).data)

	def post(self, request):
		serializer = YogaPoseSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		if serializer.validated_data.get("category") == "sequence":
			return Response({"detail": "Create sequences via /yoga/sequences."}, status=status.HTTP_400_BAD_REQUEST)
		pose = YogaPose.objects.create(**serializer.validated_data)
		return Response(YogaPoseSerializer(pose).data, status=status.HTTP_201_CREATED)


class YogaPoseDetailView(APIView):
	parser_classes = [JSONParser]

	def get_object(self, pk: int) -> YogaPose:
		pose = YogaPose.objects.exclude(category="sequence").filter(pk=pk).first()
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
		if updated.get("category") == "sequence":
			return Response({"detail": "Update sequences via /yoga/sequences/<id>."}, status=status.HTTP_400_BAD_REQUEST)

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
		poses = YogaPose.objects.exclude(category="sequence").filter(yoga_name__icontains=yoga_name)
		category = request.query_params.get("category")
		if category:
			poses = poses.filter(category__iexact=category)
		poses = poses.order_by("id")
		return Response(YogaPoseSerializer(poses, many=True).data)


class YogaSequencesView(APIView):
	parser_classes = [JSONParser]

	def get(self, request):
		sequences = YogaSequence.objects.all()
		category = request.query_params.get("category")
		if category:
			sequences = sequences.filter(category__iexact=category)
		sequences = sequences.order_by("id")
		return Response(YogaSequenceSerializer(sequences, many=True).data)

	def post(self, request):
		serializer = YogaSequenceSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		created = dict(serializer.validated_data)
		created["category"] = created.get("category") or "sequence"
		sequence = YogaSequence.objects.create(**created)
		return Response(YogaSequenceSerializer(sequence).data, status=status.HTTP_201_CREATED)


class YogaSequenceDetailView(APIView):
	parser_classes = [JSONParser]

	def get_object(self, pk: int) -> YogaSequence:
		sequence = YogaSequence.objects.filter(pk=pk).first()
		if sequence is None:
			raise Http404(f"Yoga sequence not found with id: {pk}")
		return sequence

	def get(self, request, pk: int):
		return Response(YogaSequenceSerializer(self.get_object(pk)).data)

	def put(self, request, pk: int):
		sequence = self.get_object(pk)
		serializer = YogaSequenceSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		updated = serializer.validated_data

		delete_replaced_media(
			sequence.audio_url,
			updated.get("audio_url"),
			settings.ASKNEHRU_YOGA_AUDIO_UPLOAD_DIR,
			"/media/yoga-audio/",
		)
		delete_replaced_media(
			sequence.image_url,
			updated.get("image_url"),
			settings.ASKNEHRU_YOGA_IMAGE_UPLOAD_DIR,
			"/media/yoga-poses/",
		)
		delete_replaced_media(
			sequence.video_url,
			updated.get("video_url"),
			settings.ASKNEHRU_YOGA_VIDEO_UPLOAD_DIR,
			"/media/yoga-video/",
		)

		sequence.sequence_name = updated["sequence_name"]
		sequence.blog_content = updated.get("blog_content")
		sequence.audio_url = updated.get("audio_url")
		sequence.video_url = updated.get("video_url")
		sequence.image_url = updated.get("image_url")
		sequence.category = updated.get("category") or "sequence"
		sequence.save()
		return Response(YogaSequenceSerializer(sequence).data)

	def delete(self, request, pk: int):
		sequence = self.get_object(pk)
		delete_managed_media(sequence.audio_url, settings.ASKNEHRU_YOGA_AUDIO_UPLOAD_DIR, "/media/yoga-audio/")
		delete_managed_media(sequence.image_url, settings.ASKNEHRU_YOGA_IMAGE_UPLOAD_DIR, "/media/yoga-poses/")
		delete_managed_media(sequence.video_url, settings.ASKNEHRU_YOGA_VIDEO_UPLOAD_DIR, "/media/yoga-video/")
		sequence.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)


class YogaSequencesSearchView(APIView):
	def get(self, request):
		sequence_name = request.query_params.get("sequenceName", "")
		sequences = YogaSequence.objects.filter(sequence_name__icontains=sequence_name)
		category = request.query_params.get("category")
		if category:
			sequences = sequences.filter(category__iexact=category)
		sequences = sequences.order_by("id")
		return Response(YogaSequenceSerializer(sequences, many=True).data)


class PranayamaSequencesView(APIView):
	parser_classes = [JSONParser]

	def get(self, request):
		sequences = PranayamaSequence.objects.all()
		category = request.query_params.get("category")
		if category:
			sequences = sequences.filter(category__iexact=category)
		sequences = sequences.order_by("id")
		return Response(PranayamaSequenceSerializer(sequences, many=True).data)

	def post(self, request):
		serializer = PranayamaSequenceSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		created = dict(serializer.validated_data)
		created.pop("articles", None)
		created["category"] = created.get("category") or "pranayama"
		sequence = PranayamaSequence.objects.create(**created)
		return Response(PranayamaSequenceSerializer(sequence).data, status=status.HTTP_201_CREATED)


class PranayamaSequenceDetailView(APIView):
	parser_classes = [JSONParser]

	def get_object(self, pk: int) -> PranayamaSequence:
		sequence = PranayamaSequence.objects.filter(pk=pk).first()
		if sequence is None:
			raise Http404(f"Pranayama sequence not found with id: {pk}")
		return sequence

	def get(self, request, pk: int):
		return Response(PranayamaSequenceSerializer(self.get_object(pk)).data)

	def put(self, request, pk: int):
		sequence = self.get_object(pk)
		serializer = PranayamaSequenceSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		updated = dict(serializer.validated_data)
		updated.pop("articles", None)

		delete_replaced_media(
			sequence.audio_url,
			updated.get("audio_url"),
			settings.ASKNEHRU_YOGA_AUDIO_UPLOAD_DIR,
			"/media/yoga-audio/",
		)

		sequence.name = updated["name"]
		sequence.description = updated["description"]
		sequence.steps = updated["steps"]
		sequence.duration = updated.get("duration")
		sequence.benefits = updated.get("benefits")
		sequence.contraindications = updated.get("contraindications")
		sequence.audio_url = updated.get("audio_url")
		sequence.category = updated.get("category") or "pranayama"
		sequence.save()
		return Response(PranayamaSequenceSerializer(sequence).data)

	def delete(self, request, pk: int):
		sequence = self.get_object(pk)
		delete_managed_media(sequence.audio_url, settings.ASKNEHRU_YOGA_AUDIO_UPLOAD_DIR, "/media/yoga-audio/")
		sequence.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)


class PranayamaSequencesSearchView(APIView):
	def get(self, request):
		name = request.query_params.get("name", "")
		sequences = PranayamaSequence.objects.filter(name__icontains=name)
		category = request.query_params.get("category")
		if category:
			sequences = sequences.filter(category__iexact=category)
		sequences = sequences.order_by("id")
		return Response(PranayamaSequenceSerializer(sequences, many=True).data)


class PranayamaArticlesView(APIView):
	parser_classes = [JSONParser]

	def get(self, request):
		articles = PranayamaArticle.objects.all()
		category = request.query_params.get("category")
		if category:
			articles = articles.filter(category__iexact=category)
		articles = articles.order_by("id")
		return Response(PranayamaArticleSerializer(articles, many=True).data)

	def post(self, request):
		serializer = PranayamaArticleSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		article = PranayamaArticle.objects.create(**serializer.validated_data)
		return Response(PranayamaArticleSerializer(article).data, status=status.HTTP_201_CREATED)


class PranayamaArticleDetailView(APIView):
	parser_classes = [JSONParser]

	def get_object(self, pk: int) -> PranayamaArticle:
		article = PranayamaArticle.objects.filter(pk=pk).first()
		if article is None:
			raise Http404(f"Pranayama article not found with id: {pk}")
		return article

	def get(self, request, pk: int):
		return Response(PranayamaArticleSerializer(self.get_object(pk)).data)

	def put(self, request, pk: int):
		article = self.get_object(pk)
		serializer = PranayamaArticleSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		updated = serializer.validated_data
		article.pranayama_sequence = updated["pranayama_sequence"]
		article.title = updated["title"]
		article.content = updated["content"]
		article.category = updated.get("category")
		article.save()
		return Response(PranayamaArticleSerializer(article).data)

	def delete(self, request, pk: int):
		article = self.get_object(pk)
		article.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)


class PranayamaArticlesSearchView(APIView):
	def get(self, request):
		title = request.query_params.get("title", "")
		articles = PranayamaArticle.objects.filter(title__icontains=title)
		category = request.query_params.get("category")
		if category:
			articles = articles.filter(category__iexact=category)
		articles = articles.order_by("id")
		return Response(PranayamaArticleSerializer(articles, many=True).data)


__all__ = [
	"YogaPoseDetailView",
	"YogaPosesSearchView",
	"YogaPosesView",
	"PranayamaArticleDetailView",
	"PranayamaArticlesSearchView",
	"PranayamaArticlesView",
	"PranayamaSequenceDetailView",
	"PranayamaSequencesSearchView",
	"PranayamaSequencesView",
	"YogaSequenceDetailView",
	"YogaSequencesSearchView",
	"YogaSequencesView",
]
