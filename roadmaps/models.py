from django.db import models


class Roadmap(models.Model):
	id = models.BigAutoField(primary_key=True)
	created_at = models.DateTimeField(db_column="created_at", blank=True, null=True)
	image_url = models.CharField(max_length=500, db_column="image_url", blank=True, null=True)
	intro = models.CharField(max_length=100, blank=True, null=True)
	main_topic = models.CharField(max_length=200, db_column="main_topic")
	router_link = models.CharField(max_length=200, db_column="router_link", blank=True, null=True)
	syllabus = models.TextField(blank=True, null=True)
	updated_at = models.DateTimeField(db_column="updated_at", blank=True, null=True)

	class Meta:
		managed = False
		db_table = "roadmaps"


__all__ = ["Roadmap"]
