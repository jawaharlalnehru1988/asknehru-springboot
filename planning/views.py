from django.db.models import Q
from rest_framework import viewsets

from .models import Epic, Task

from .serializers import EpicSerializer, TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
	serializer_class = TaskSerializer

	def get_queryset(self):
		queryset = Task.objects.select_related("assigned_to", "created_by", "epic").order_by("-updated_at", "-id")

		if self.request.user and self.request.user.is_authenticated:
			user = self.request.user
			queryset = queryset.filter(
				Q(epic__members__user=user) |
				Q(assigned_to=user) |
				Q(created_by=user)
			).distinct()
		else:
			queryset = queryset.none()

		status_filter = self.request.query_params.get("status")
		if status_filter:
			queryset = queryset.filter(status=status_filter)
		return queryset

	def perform_create(self, serializer):
		serializer.save(created_by=self.request.user)


class EpicViewSet(viewsets.ModelViewSet):
	serializer_class = EpicSerializer

	def get_queryset(self):
		if self.request.user and self.request.user.is_authenticated:
			queryset = Epic.objects.filter(members__user=self.request.user).order_by("-updated_at", "-id")
		else:
			queryset = Epic.objects.none()
		return queryset


__all__ = ["EpicViewSet", "TaskViewSet"]
