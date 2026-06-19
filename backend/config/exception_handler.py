from django.db.models import ProtectedError
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    if isinstance(exc, ProtectedError):
        return Response(
            {"detail": "No se puede eliminar: tiene registros asociados que dependen de este elemento."},
            status=409,
        )
    return exception_handler(exc, context)
