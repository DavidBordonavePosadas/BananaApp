from rest_framework import viewsets

from .models import Parcela
from .serializers import ParcelaSerializer


class ParcelaViewSet(viewsets.ModelViewSet):
    queryset = Parcela.objects.all()
    serializer_class = ParcelaSerializer
