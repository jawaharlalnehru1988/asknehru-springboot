from django.db import models


class YogaPose(models.Model):
	id = models.BigAutoField(primary_key=True)
	yoga_name = models.CharField(max_length=255, db_column="yoga_name")
	yoga_name_english = models.CharField(max_length=255, db_column="yoga_name_english", blank=True, null=True)
	blog_content = models.CharField(max_length=10000, db_column="blog_content", blank=True, null=True)
	audio_url = models.CharField(max_length=1000, db_column="audio_url", blank=True, null=True)
	video_url = models.CharField(max_length=1000, db_column="video_url", blank=True, null=True)
	image_url = models.CharField(max_length=1000, db_column="image_url", blank=True, null=True)
	category = models.CharField(max_length=255, blank=True, null=True)

	class Meta:
		managed = False
		db_table = "yoga_poses"


class YogaSequence(models.Model):
	id = models.BigAutoField(primary_key=True)
	sequence_name = models.CharField(max_length=255, db_column="sequence_name")
	blog_content = models.CharField(max_length=10000, db_column="blog_content", blank=True, null=True)
	audio_url = models.CharField(max_length=1000, db_column="audio_url", blank=True, null=True)
	video_url = models.CharField(max_length=1000, db_column="video_url", blank=True, null=True)
	image_url = models.CharField(max_length=1000, db_column="image_url", blank=True, null=True)
	category = models.CharField(max_length=255, blank=True, null=True)

	class Meta:
		db_table = "yoga_sequences"


class PranayamaSequence(models.Model):
	id = models.BigAutoField(primary_key=True)
	name = models.CharField(max_length=255)
	description = models.TextField()
	steps = models.TextField()
	duration = models.CharField(max_length=120, blank=True, null=True)
	benefits = models.TextField(blank=True, null=True)
	contraindications = models.TextField(blank=True, null=True)
	audio_url = models.CharField(max_length=1000, blank=True, null=True)
	category = models.CharField(max_length=255, blank=True, null=True)

	class Meta:
		db_table = "pranayama_sequences"


class PranayamaArticle(models.Model):
	id = models.BigAutoField(primary_key=True)
	pranayama_sequence = models.ForeignKey(
		PranayamaSequence,
		on_delete=models.CASCADE,
		related_name="articles",
	)
	title = models.CharField(max_length=255)
	content = models.TextField()
	category = models.CharField(max_length=255, blank=True, null=True)

	class Meta:
		db_table = "pranayama_articles"


__all__ = ["PranayamaArticle", "PranayamaSequence", "YogaPose", "YogaSequence"]
