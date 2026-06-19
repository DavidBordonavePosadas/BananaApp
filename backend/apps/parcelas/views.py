from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Parcela
from .serializers import ParcelaSerializer


class ParcelaViewSet(viewsets.ModelViewSet):
    serializer_class = ParcelaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Parcela.objects.all()
        activa = self.request.query_params.get("activa")
        if activa is not None:
            qs = qs.filter(activa=activa.lower() == "true")
        return qs
