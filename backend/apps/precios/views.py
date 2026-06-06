from rest_framework import viewsets

from .models import HistorialPrecio
from .serializers import HistorialPrecioSerializer


class HistorialPrecioViewSet(viewsets.ModelViewSet):
    queryset = HistorialPrecio.objects.all()
    serializer_class = HistorialPrecioSerializer
