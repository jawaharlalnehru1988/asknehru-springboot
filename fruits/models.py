from django.db import models


class FruitGallery(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "fruits_gallery"
        ordering = ["id"]


class FruitGalleryImage(models.Model):
    fruit = models.ForeignKey(FruitGallery, on_delete=models.CASCADE, related_name="images")
    image_path = models.CharField(max_length=1000)

    class Meta:
        db_table = "fruits_gallery_images"
        ordering = ["id"]


__all__ = ["FruitGallery", "FruitGalleryImage"]
