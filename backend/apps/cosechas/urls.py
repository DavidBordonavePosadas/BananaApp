from rest_framework.routers import DefaultRouter

from .views import CosechaViewSet

router = DefaultRouter()
router.register(r"", CosechaViewSet, basename="cosecha")

urlpatterns = router.urls
