from rest_framework import serializers

from .models import Medicine
from core.serializer_utils import MEDICINE_CATEGORIES


class MedicineWriteSerializer(serializers.Serializer):
	name = serializers.CharField(required=False, trim_whitespace=True)
	brand = serializers.CharField(required=False, allow_blank=True, allow_null=True)
	category = serializers.CharField(required=False, trim_whitespace=True)
	quantity = serializers.IntegerField(required=False, min_value=1)
	unit = serializers.CharField(required=False, allow_blank=True, allow_null=True)
	expiryDate = serializers.DateField(required=False)
	manufactureDate = serializers.DateField(required=False, allow_null=True)
	description = serializers.CharField(required=False, allow_blank=True, allow_null=True)
	dosageInstructions = serializers.CharField(required=False, allow_blank=True, allow_null=True)
	ingredients = serializers.ListField(child=serializers.CharField(), required=False)
	sideEffects = serializers.ListField(child=serializers.CharField(), required=False)
	benefits = serializers.ListField(child=serializers.CharField(), required=False)
	location = serializers.CharField(required=False, allow_blank=True, allow_null=True)

	def validate_category(self, value):
		normalized = value.strip().upper()
		if normalized not in MEDICINE_CATEGORIES:
			raise serializers.ValidationError("Invalid medicine category.")
		return normalized

	def validate(self, attrs):
		if not self.partial:
			required_fields = ["name", "category", "quantity", "expiryDate"]
			missing_fields = [field for field in required_fields if field not in attrs]
			if missing_fields:
				raise serializers.ValidationError({field: ["This field is required."] for field in missing_fields})

		if "name" in attrs:
			attrs["name"] = attrs["name"].strip()
		if "brand" in attrs and attrs["brand"] is not None:
			attrs["brand"] = attrs["brand"].strip()
		if "unit" in attrs and attrs["unit"] is not None:
			attrs["unit"] = attrs["unit"].strip()
		if "location" in attrs and attrs["location"] is not None:
			attrs["location"] = attrs["location"].strip()
		return attrs


class MedicineResponseSerializer(serializers.ModelSerializer):
	expiryDate = serializers.DateField(source="expiry_date")
	manufactureDate = serializers.DateField(source="manufacture_date", allow_null=True)
	dosageInstructions = serializers.CharField(source="dosage_instructions", allow_null=True)
	createdAt = serializers.DateTimeField(source="created_at")
	lastUpdated = serializers.DateTimeField(source="last_updated")
	ingredients = serializers.ListField(child=serializers.CharField(), read_only=True)
	sideEffects = serializers.ListField(child=serializers.CharField(), read_only=True)
	benefits = serializers.ListField(child=serializers.CharField(), read_only=True)

	class Meta:
		model = Medicine
		fields = [
			"id",
			"name",
			"brand",
			"category",
			"quantity",
			"unit",
			"expiryDate",
			"manufactureDate",
			"description",
			"dosageInstructions",
			"ingredients",
			"sideEffects",
			"benefits",
			"location",
			"createdAt",
			"lastUpdated",
		]


__all__ = ["MedicineResponseSerializer", "MedicineWriteSerializer"]
