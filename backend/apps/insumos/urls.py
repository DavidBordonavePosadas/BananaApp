from rest_framework.routers import DefaultRouter

from .views import CompraInsumoViewSet, TipoInsumoViewSet

router = DefaultRouter()
router.register(r"tipos", TipoInsumoViewSet)
router.register(r"compras", CompraInsumoViewSet)

urlpatterns = router.urls
