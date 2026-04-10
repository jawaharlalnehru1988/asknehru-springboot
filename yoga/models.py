from django.db import models


class YogaPose(models.Model):
	id = models.BigAutoField(primary_key=True)
	yoga_name = models.CharField(max_length=255, db_column="yoga_name")
	blog_content = models.CharField(max_length=10000, db_column="blog_content", blank=True, null=True)
	audio_url = models.CharField(max_length=1000, db_column="audio_url", blank=True, null=True)
	video_url = models.CharField(max_length=1000, db_column="video_url", blank=True, null=True)
	image_url = models.CharField(max_length=1000, db_column="image_url", blank=True, null=True)
	category = models.CharField(max_length=255, blank=True, null=True)

	class Meta:
		managed = False
		db_table = "yoga_poses"


__all__ = ["YogaPose"]
