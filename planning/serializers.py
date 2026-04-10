from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Epic, EpicAccess, Task


class EpicSerializer(serializers.ModelSerializer):
	clientName = serializers.CharField(source="client_name", allow_blank=True, allow_null=True, required=False)

	class Meta:
		model = Epic
		fields = ["id", "title", "clientName", "created_at", "updated_at"]


class TaskSerializer(serializers.ModelSerializer):
	assigned_to = serializers.PrimaryKeyRelatedField(
		queryset=User.objects.all(),
		allow_null=True,
		required=False,
	)
	epic = serializers.PrimaryKeyRelatedField(
		queryset=Epic.objects.all(),
		allow_null=True,
		required=False,
	)

	class Meta:
		model = Task
		fields = [
			"id",
			"title",
			"description",
			"status",
			"priority",
			"start_date",
			"due_date",
			"assigned_to",
			"epic",
			"created_at",
			"updated_at",
		]


class EpicAccessSerializer(serializers.ModelSerializer):
	username = serializers.CharField(source="user.username", read_only=True)
	user_id = serializers.IntegerField(source="user.id", read_only=True)
	epic_id = serializers.IntegerField(source="epic.id")
	user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

	class Meta:
		model = EpicAccess
		fields = ["id", "epic_id", "user", "user_id", "username", "role", "created_at"]
		read_only_fields = ["id", "created_at"]


__all__ = ["EpicAccessSerializer", "EpicSerializer", "TaskSerializer"]
