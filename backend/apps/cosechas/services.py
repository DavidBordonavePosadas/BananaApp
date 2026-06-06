from rest_framework import serializers


def set_creado_por(serializer: serializers.Serializer, user: object) -> None:
    serializer.save(creado_por=user)
