from rest_framework.routers import DefaultRouter

from .views import NotaViewSet

router = DefaultRouter()
router.register(r"", NotaViewSet)

urlpatterns = router.urls
