from rest_framework.routers import DefaultRouter

from .views import VentaViewSet

router = DefaultRouter()
router.register(r"", VentaViewSet)

urlpatterns = router.urls
