from datetime import timedelta

from django.http import Http404
from django.utils import timezone
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Medicine
from core.view_utils import (
    attach_medicine_collections,
    attach_medicine_collections_single,
    set_medicine_values,
)

from .serializers import MedicineResponseSerializer, MedicineWriteSerializer


class MedicinesView(APIView):
    parser_classes = [JSONParser]

    def get(self, request):
        medicines = attach_medicine_collections(list(Medicine.objects.order_by("id")))
        return Response(MedicineResponseSerializer(medicines, many=True).data)

    def post(self, request):
        serializer = MedicineWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        now = timezone.now()
        medicine = Medicine.objects.create(
            name=data["name"],
            brand=data.get("brand"),
            category=data["category"],
            quantity=data["quantity"],
            unit=data.get("unit") or "Tablets",
            expiry_date=data["expiryDate"],
            manufacture_date=data.get("manufactureDate"),
            description=data.get("description"),
            dosage_instructions=data.get("dosageInstructions"),
            location=data.get("location"),
            created_at=now,
            last_updated=now,
        )
        set_medicine_values(medicine.id, "medicine_ingredients", "ingredient", data.get("ingredients", []))
        set_medicine_values(medicine.id, "medicine_side_effects", "side_effect", data.get("sideEffects", []))
        set_medicine_values(medicine.id, "medicine_benefits", "benefit", data.get("benefits", []))
        return Response(MedicineResponseSerializer(attach_medicine_collections_single(medicine)).data, status=status.HTTP_201_CREATED)


class MedicineDetailView(APIView):
    parser_classes = [JSONParser]

    def get_object(self, pk: int) -> Medicine:
        medicine = Medicine.objects.filter(pk=pk).first()
        if medicine is None:
            raise Http404(f"Medicine not found with id: {pk}")
        return medicine

    def get(self, request, pk: int):
        return Response(MedicineResponseSerializer(attach_medicine_collections_single(self.get_object(pk))).data)

    def put(self, request, pk: int):
        medicine = self.get_object(pk)
        serializer = MedicineWriteSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        if "name" in data:
            medicine.name = data["name"]
        if "brand" in data:
            medicine.brand = data["brand"]
        if "category" in data:
            medicine.category = data["category"]
        if "quantity" in data:
            medicine.quantity = data["quantity"]
        if "unit" in data:
            medicine.unit = data["unit"]
        if "expiryDate" in data:
            medicine.expiry_date = data["expiryDate"]
        if "manufactureDate" in data:
            medicine.manufacture_date = data["manufactureDate"]
        if "description" in data:
            medicine.description = data["description"]
        if "dosageInstructions" in data:
            medicine.dosage_instructions = data["dosageInstructions"]
        if "location" in data:
            medicine.location = data["location"]

        medicine.last_updated = timezone.now()
        medicine.save()

        if "ingredients" in data:
            set_medicine_values(medicine.id, "medicine_ingredients", "ingredient", data["ingredients"])
        if "sideEffects" in data:
            set_medicine_values(medicine.id, "medicine_side_effects", "side_effect", data["sideEffects"])
        if "benefits" in data:
            set_medicine_values(medicine.id, "medicine_benefits", "benefit", data["benefits"])

        return Response(MedicineResponseSerializer(attach_medicine_collections_single(medicine)).data)

    def delete(self, request, pk: int):
        medicine = self.get_object(pk)
        medicine.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MedicinesByCategoryView(APIView):
    def get(self, request, category: str):
        medicines = attach_medicine_collections(list(Medicine.objects.filter(category__iexact=category).order_by("id")))
        return Response(MedicineResponseSerializer(medicines, many=True).data)


class MedicinesSearchView(APIView):
    def get(self, request):
        name = request.query_params.get("name", "")
        medicines = attach_medicine_collections(list(Medicine.objects.filter(name__icontains=name).order_by("id")))
        return Response(MedicineResponseSerializer(medicines, many=True).data)


class MedicinesExpiringSoonView(APIView):
    def get(self, request):
        days = int(request.query_params.get("days", 30))
        today = timezone.localdate()
        future_date = today + timedelta(days=days)
        medicines = attach_medicine_collections(list(Medicine.objects.filter(expiry_date__range=(today, future_date)).order_by("id")))
        return Response(MedicineResponseSerializer(medicines, many=True).data)


class MedicinesExpiredView(APIView):
    def get(self, request):
        today = timezone.localdate()
        medicines = attach_medicine_collections(list(Medicine.objects.filter(expiry_date__lt=today).order_by("id")))
        return Response(MedicineResponseSerializer(medicines, many=True).data)


class MedicinesLowStockView(APIView):
    def get(self, request):
        threshold = int(request.query_params.get("threshold", 10))
        medicines = attach_medicine_collections(list(Medicine.objects.filter(quantity__lte=threshold).order_by("id")))
        return Response(MedicineResponseSerializer(medicines, many=True).data)


__all__ = [
    "MedicineDetailView",
    "MedicinesByCategoryView",
    "MedicinesExpiredView",
    "MedicinesExpiringSoonView",
    "MedicinesLowStockView",
    "MedicinesSearchView",
    "MedicinesView",
]
