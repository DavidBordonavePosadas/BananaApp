from rest_framework import serializers

from .models import Cosecha


class CosechaSerializer(serializers.ModelSerializer):
    total_estimado = serializers.ReadOnlyField()
    parcela_nombre = serializers.CharField(source="parcela.nombre", read_only=True)

    class Meta:
        model = Cosecha
        fields = [
            "id",
            "parcela",
            "parcela_nombre",
            "creado_por",
            "fecha",
            "racimos_cortados",
            "rejas_producidas",
            "peso_kg",
            "precio_kg",
            "notas",
            "total_estimado",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["creado_por", "created_at", "updated_at"]


class ProduccionPorParcelaSerializer(serializers.Serializer):
    parcela_id = serializers.IntegerField()
    parcela_nombre = serializers.CharField()
    total_peso = serializers.DecimalField(max_digits=12, decimal_places=2, allow_null=True)
    total_valor = serializers.DecimalField(max_digits=14, decimal_places=2, allow_null=True)


class ProduccionMensualSerializer(serializers.Serializer):
    mes = serializers.IntegerField()
    total_peso = serializers.DecimalField(max_digits=12, decimal_places=2, allow_null=True)
    total_valor = serializers.DecimalField(max_digits=14, decimal_places=2, allow_null=True)


class ProduccionSemanalSerializer(serializers.Serializer):
    semana = serializers.DateField()
    total_peso = serializers.DecimalField(max_digits=12, decimal_places=2, allow_null=True)
    total_valor = serializers.DecimalField(max_digits=14, decimal_places=2, allow_null=True)


class TopParcelaSerializer(serializers.Serializer):
    parcela_id = serializers.IntegerField()
    parcela_nombre = serializers.CharField()
    total_peso = serializers.DecimalField(max_digits=12, decimal_places=2)


class ResumenPeriodoSerializer(serializers.Serializer):
    total_peso = serializers.DecimalField(max_digits=12, decimal_places=2, allow_null=True)
    total_valor = serializers.DecimalField(max_digits=14, decimal_places=2, allow_null=True)
    num_cosechas = serializers.IntegerField()
    top_parcela = TopParcelaSerializer(allow_null=True)
