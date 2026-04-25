from django.contrib.auth.models import User
from rest_framework import serializers
import re

from .models import Epic, EpicAccess, Task


class EpicSerializer(serializers.ModelSerializer):
	clientName = serializers.CharField(source="client_name", allow_blank=True, allow_null=True, required=False)

	class Meta:
		model = Epic
		fields = ["id", "title", "clientName", "created_at", "updated_at"]


class TaskSerializer(serializers.ModelSerializer):
	effort_time = serializers.CharField(required=False, allow_blank=True, allow_null=True, write_only=True)
	assigned_to = serializers.PrimaryKeyRelatedField(
		queryset=User.objects.all(),
		allow_null=True,
		required=False,
	)
	assigned_to_username = serializers.CharField(source="assigned_to.username", read_only=True)
	created_by = serializers.PrimaryKeyRelatedField(read_only=True)
	created_by_username = serializers.CharField(source="created_by.username", read_only=True)
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
			"effort_time",
			"start_date",
			"due_date",
			"assigned_to",
			"assigned_to_username",
			"created_by",
			"created_by_username",
			"epic",
			"created_at",
			"updated_at",
		]

	def validate(self, attrs):
		effort_time = attrs.pop("effort_time", serializers.empty)
		if effort_time is not serializers.empty:
			if effort_time in (None, ""):
				attrs["effort_minutes"] = None
			else:
				if not isinstance(effort_time, str) or not re.fullmatch(r"(?:[01]\d|2[0-3]):[0-5]\d", effort_time):
					raise serializers.ValidationError({"effort_time": "Use HH:MM in 24-hour format (e.g. 23:40)."})
				hours, minutes = map(int, effort_time.split(":"))
				attrs["effort_minutes"] = hours * 60 + minutes
		return attrs

	def to_representation(self, instance):
		data = super().to_representation(instance)
		effort_minutes = instance.effort_minutes
		if effort_minutes is None and instance.effort_hours is not None:
			effort_minutes = instance.effort_hours * 60
		if effort_minutes is None:
			data["effort_time"] = None
		else:
			hours = effort_minutes // 60
			minutes = effort_minutes % 60
			data["effort_time"] = f"{hours:02d}:{minutes:02d}"
		return data


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
