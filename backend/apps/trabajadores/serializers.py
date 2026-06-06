from rest_framework import serializers

from .models import Actividad, RegistroTrabajo, Trabajador


class TrabajadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trabajador
        fields = "__all__"


class ActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actividad
        fields = "__all__"


class RegistroTrabajoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroTrabajo
        fields = "__all__"
        read_only_fields = ["created_at"]
