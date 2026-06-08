from rest_framework import serializers

from .models import HistorialPrecio


class HistorialPrecioSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialPrecio
        fields = ["id", "fecha", "precio_kg", "notas", "created_at"]
        read_only_fields = ["created_at"]


class _PrecioExtremoSerializer(serializers.Serializer):
    precio_kg = serializers.DecimalField(max_digits=8, decimal_places=2)
    fecha = serializers.DateField()


class EstadisticasSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    promedio = serializers.DecimalField(max_digits=8, decimal_places=2, allow_null=True)
    maximo = _PrecioExtremoSerializer(allow_null=True)
    minimo = _PrecioExtremoSerializer(allow_null=True)


class TendenciaMensualItemSerializer(serializers.Serializer):
    mes = serializers.IntegerField()
    promedio = serializers.DecimalField(max_digits=8, decimal_places=2, allow_null=True)


class _PeriodoStatsSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    promedio = serializers.DecimalField(max_digits=8, decimal_places=2, allow_null=True)
    maximo = _PrecioExtremoSerializer(allow_null=True)
    minimo = _PrecioExtremoSerializer(allow_null=True)


class ComparacionPeriodosSerializer(serializers.Serializer):
    periodo_1 = _PeriodoStatsSerializer()
    periodo_2 = _PeriodoStatsSerializer()
    diferencia_porcentual = serializers.DecimalField(
        max_digits=12, decimal_places=4, allow_null=True
    )
