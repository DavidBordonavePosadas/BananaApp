from rest_framework.routers import DefaultRouter

from .views import HistorialPrecioViewSet

router = DefaultRouter()
router.register(r"", HistorialPrecioViewSet)

urlpatterns = router.urls
