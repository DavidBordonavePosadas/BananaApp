from rest_framework import serializers

from .models import Parcela


class ParcelaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcela
        fields = [
            "id",
            "nombre",
            "area_hectareas",
            "activa",
            "notas",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]
