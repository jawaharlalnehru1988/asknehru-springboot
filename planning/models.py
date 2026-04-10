from django.contrib.auth.models import User
from django.db import models


class Epic(models.Model):
	title = models.CharField(max_length=255)
	client_name = models.CharField(max_length=255, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = "api_epic"
		managed = False

	def __str__(self):
		return self.title


class Task(models.Model):
	PRIORITY_CHOICES = [
		("Critical", "Critical"),
		("High", "High"),
		("Medium", "Medium"),
		("Low", "Low"),
	]

	STATUS_CHOICES = [
		("Backlog", "Backlog"),
		("To Do", "To Do"),
		("In Progress", "In Progress"),
		("Completed", "Completed"),
	]

	title = models.CharField(max_length=255)
	description = models.TextField(blank=True, null=True)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="To Do")
	priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default="Medium")
	start_date = models.DateTimeField(blank=True, null=True)
	due_date = models.DateTimeField()
	assigned_to = models.ForeignKey(
		User,
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name="tasks",
	)
	epic = models.ForeignKey(Epic, on_delete=models.CASCADE, null=True, blank=True, related_name="tasks")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = "api_task"
		managed = False

	def __str__(self):
		return f"{self.title} ({self.status})"


class EpicAccess(models.Model):
	ROLE_CHOICES = [
		("viewer", "Viewer"),
		("editor", "Editor"),
		("owner", "Owner"),
	]

	epic = models.ForeignKey(Epic, on_delete=models.CASCADE, related_name="members")
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="epic_access")
	role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="viewer")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = "api_epicaccess"
		managed = False
		unique_together = ("epic", "user")
		verbose_name = "Epic Access"
		verbose_name_plural = "Epic Accesses"

	def __str__(self):
		return f"{self.user.username} -> {self.epic.title} ({self.role})"


__all__ = ["Epic", "EpicAccess", "Task"]
