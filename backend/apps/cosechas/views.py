from rest_framework import viewsets

from .models import Cosecha
from .serializers import CosechaSerializer
from .services import set_creado_por


class CosechaViewSet(viewsets.ModelViewSet):
    queryset = Cosecha.objects.select_related("parcela", "creado_por").all()
    serializer_class = CosechaSerializer

    def perform_create(self, serializer: CosechaSerializer) -> None:
        set_creado_por(serializer, self.request.user)
