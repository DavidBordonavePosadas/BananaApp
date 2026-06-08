from rest_framework import serializers

from .models import CompraInsumo, TipoInsumo


class TipoInsumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoInsumo
        fields = "__all__"


class CompraInsumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompraInsumo
        fields = "__all__"
        read_only_fields = ["creado_por", "created_at", "updated_at"]
