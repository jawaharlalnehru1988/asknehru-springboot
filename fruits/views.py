from django.db import transaction
from django.http import Http404
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import FruitGallery, FruitGalleryImage
from .serializers import FruitGalleryResponseSerializer, FruitGalleryWriteSerializer


class FruitsGalleryView(APIView):
    parser_classes = [JSONParser]

    def get(self, request):
        fruits = FruitGallery.objects.prefetch_related("images").order_by("id")
        return Response(FruitGalleryResponseSerializer(fruits, many=True).data)

    @transaction.atomic
    def post(self, request):
        serializer = FruitGalleryWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        fruit = FruitGallery.objects.create(
            name=data["name"],
            price=data["price"],
            discount_percentage=data.get("discountPercentage", 0),
            description=data.get("description"),
        )
        FruitGalleryImage.objects.bulk_create(
            [FruitGalleryImage(fruit=fruit, image_path=image_path) for image_path in data["imagePath"]]
        )

        fruit = FruitGallery.objects.prefetch_related("images").get(pk=fruit.pk)
        return Response(FruitGalleryResponseSerializer(fruit).data, status=status.HTTP_201_CREATED)


class FruitGalleryDetailView(APIView):
    parser_classes = [JSONParser]

    def get_object(self, pk: int) -> FruitGallery:
        fruit = FruitGallery.objects.prefetch_related("images").filter(pk=pk).first()
        if fruit is None:
            raise Http404(f"Fruit gallery not found with id: {pk}")
        return fruit

    def get(self, request, pk: int):
        return Response(FruitGalleryResponseSerializer(self.get_object(pk)).data)

    @transaction.atomic
    def put(self, request, pk: int):
        fruit = self.get_object(pk)
        serializer = FruitGalleryWriteSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        if "name" in data:
            fruit.name = data["name"]
        if "price" in data:
            fruit.price = data["price"]
        if "discountPercentage" in data:
            fruit.discount_percentage = data["discountPercentage"]
        if "description" in data:
            fruit.description = data["description"]
        fruit.save()

        if "imagePath" in data:
            fruit.images.all().delete()
            FruitGalleryImage.objects.bulk_create(
                [FruitGalleryImage(fruit=fruit, image_path=image_path) for image_path in data["imagePath"]]
            )

        fruit = FruitGallery.objects.prefetch_related("images").get(pk=fruit.pk)
        return Response(FruitGalleryResponseSerializer(fruit).data)

    @transaction.atomic
    def delete(self, request, pk: int):
        fruit = self.get_object(pk)
        fruit.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


__all__ = ["FruitGalleryDetailView", "FruitsGalleryView"]
