from django.db import models


class Medicine(models.Model):
	id = models.BigAutoField(primary_key=True)
	brand = models.CharField(max_length=200, blank=True, null=True)
	category = models.CharField(max_length=100)
	created_at = models.DateTimeField(db_column="created_at")
	description = models.TextField(blank=True, null=True)
	dosage_instructions = models.TextField(db_column="dosage_instructions", blank=True, null=True)
	expiry_date = models.DateField(db_column="expiry_date")
	last_updated = models.DateTimeField(db_column="last_updated")
	location = models.CharField(max_length=200, blank=True, null=True)
	manufacture_date = models.DateField(db_column="manufacture_date", blank=True, null=True)
	name = models.CharField(max_length=200)
	quantity = models.IntegerField()
	unit = models.CharField(max_length=50, blank=True, null=True)

	class Meta:
		managed = False
		db_table = "medicines"


__all__ = ["Medicine"]
