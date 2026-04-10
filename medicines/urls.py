from django.urls import path

from .views import (
    MedicineDetailView,
    MedicinesByCategoryView,
    MedicinesExpiredView,
    MedicinesExpiringSoonView,
    MedicinesLowStockView,
    MedicinesSearchView,
    MedicinesView,
)


urlpatterns = [
    path("medicines", MedicinesView.as_view()),
    path("medicines/category/<str:category>", MedicinesByCategoryView.as_view()),
    path("medicines/search", MedicinesSearchView.as_view()),
    path("medicines/expiring-soon", MedicinesExpiringSoonView.as_view()),
    path("medicines/expired", MedicinesExpiredView.as_view()),
    path("medicines/low-stock", MedicinesLowStockView.as_view()),
    path("medicines/<int:pk>", MedicineDetailView.as_view()),
]
