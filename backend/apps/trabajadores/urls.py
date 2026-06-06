from rest_framework.routers import DefaultRouter

from .views import ActividadViewSet, RegistroTrabajoViewSet, TrabajadorViewSet

router = DefaultRouter()
router.register(r"trabajadores", TrabajadorViewSet)
router.register(r"actividades", ActividadViewSet)
router.register(r"registros", RegistroTrabajoViewSet)

urlpatterns = router.urls
