from rest_framework import serializers

from .models import FruitGallery, FruitGalleryImage


class FruitGalleryWriteSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, trim_whitespace=True, max_length=200)
    price = serializers.DecimalField(required=False, max_digits=10, decimal_places=2, min_value=0)
    discountPercentage = serializers.DecimalField(
        required=False,
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=100,
    )
    description = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    imagePath = serializers.ListField(child=serializers.CharField(trim_whitespace=True, max_length=1000), required=False)

    def validate(self, attrs):
        if not self.partial:
            required_fields = ["name", "price", "discountPercentage", "description", "imagePath"]
            missing_fields = [field for field in required_fields if field not in attrs]
            if missing_fields:
                raise serializers.ValidationError({field: ["This field is required."] for field in missing_fields})

        if "name" in attrs:
            attrs["name"] = attrs["name"].strip()

        if "description" in attrs and attrs["description"] is not None:
            attrs["description"] = attrs["description"].strip()

        if "imagePath" in attrs:
            clean_paths = [path.strip() for path in attrs["imagePath"] if path and path.strip()]
            if not clean_paths:
                raise serializers.ValidationError({"imagePath": ["At least one image path is required."]})
            attrs["imagePath"] = clean_paths

        return attrs


class FruitGalleryResponseSerializer(serializers.ModelSerializer):
    discountPercentage = serializers.DecimalField(source="discount_percentage", max_digits=5, decimal_places=2)
    imagePath = serializers.SerializerMethodField()

    class Meta:
        model = FruitGallery
        fields = [
            "id",
            "name",
            "price",
            "discountPercentage",
            "description",
            "imagePath",
            "created_at",
            "updated_at",
        ]

    def get_imagePath(self, obj):
        return [image.image_path for image in obj.images.all().order_by("id")]


__all__ = ["FruitGalleryResponseSerializer", "FruitGalleryWriteSerializer"]
