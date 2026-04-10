from django.db import models


class Conversation(models.Model):
	id = models.BigAutoField(primary_key=True)
	article = models.TextField()
	article_audio = models.CharField(max_length=500, db_column="article_audio", blank=True, null=True)
	conversation_audio = models.CharField(max_length=500, db_column="conversation_audio", blank=True, null=True)
	created_at = models.DateTimeField(db_column="created_at")
	main_topic = models.CharField(max_length=100, db_column="main_topic")
	negative_conversation = models.TextField(db_column="negative_conversation", blank=True, null=True)
	positive_conversation = models.TextField(db_column="positive_conversation", blank=True, null=True)
	sub_topic = models.CharField(max_length=200, db_column="sub_topic")
	updated_at = models.DateTimeField(db_column="updated_at")

	class Meta:
		managed = False
		db_table = "knowledge_base"


__all__ = ["Conversation"]
