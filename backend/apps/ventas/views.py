from rest_framework import viewsets

from .models import Venta
from .serializers import VentaSerializer


class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.select_related("cliente").all()
    serializer_class = VentaSerializer
