from rest_framework import serializers

from .models import Nota


class NotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nota
        fields = "__all__"
        read_only_fields = ["creado_por", "created_at", "updated_at"]
