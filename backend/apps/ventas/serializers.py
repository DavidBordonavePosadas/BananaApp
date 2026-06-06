from rest_framework import serializers

from .models import Venta


class VentaSerializer(serializers.ModelSerializer):
    total = serializers.ReadOnlyField()
    estado_pago = serializers.ReadOnlyField()

    class Meta:
        model = Venta
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at"]
