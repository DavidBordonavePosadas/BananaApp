from rest_framework import viewsets

from .models import Nota
from .serializers import NotaSerializer
from .services import set_creado_por


class NotaViewSet(viewsets.ModelViewSet):
    queryset = Nota.objects.select_related("creado_por").all()
    serializer_class = NotaSerializer

    def perform_create(self, serializer: NotaSerializer) -> None:
        set_creado_por(serializer, self.request.user)
