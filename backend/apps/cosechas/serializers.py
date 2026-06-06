from rest_framework import serializers

from .models import Cosecha


class CosechaSerializer(serializers.ModelSerializer):
    total_estimado = serializers.ReadOnlyField()

    class Meta:
        model = Cosecha
        fields = "__all__"
        read_only_fields = ["creado_por", "created_at", "updated_at"]
