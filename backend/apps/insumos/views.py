from rest_framework import viewsets

from .models import CompraInsumo, TipoInsumo
from .serializers import CompraInsumoSerializer, TipoInsumoSerializer
from .services import set_creado_por


class TipoInsumoViewSet(viewsets.ModelViewSet):
    queryset = TipoInsumo.objects.all()
    serializer_class = TipoInsumoSerializer


class CompraInsumoViewSet(viewsets.ModelViewSet):
    queryset = CompraInsumo.objects.select_related("tipo_insumo", "creado_por").all()
    serializer_class = CompraInsumoSerializer

    def perform_create(self, serializer: CompraInsumoSerializer) -> None:
        set_creado_por(serializer, self.request.user)
