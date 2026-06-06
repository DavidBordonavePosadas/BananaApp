from rest_framework import viewsets

from .models import Actividad, RegistroTrabajo, Trabajador
from .serializers import ActividadSerializer, RegistroTrabajoSerializer, TrabajadorSerializer


class TrabajadorViewSet(viewsets.ModelViewSet):
    queryset = Trabajador.objects.all()
    serializer_class = TrabajadorSerializer


class ActividadViewSet(viewsets.ModelViewSet):
    queryset = Actividad.objects.all()
    serializer_class = ActividadSerializer


class RegistroTrabajoViewSet(viewsets.ModelViewSet):
    queryset = RegistroTrabajo.objects.select_related(
        "trabajador", "parcela", "actividad"
    ).all()
    serializer_class = RegistroTrabajoSerializer
