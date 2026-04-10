from rest_framework.routers import DefaultRouter

from .views import EpicViewSet, TaskViewSet


router = DefaultRouter()
router.register("tasks", TaskViewSet, basename="task")
router.register("epics", EpicViewSet, basename="epic")

urlpatterns = router.urls
