from __future__ import annotations

from datetime import date

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response

from . import services
from .models import HistorialPrecio
from .serializers import (
    ComparacionPeriodosSerializer,
    EstadisticasSerializer,
    HistorialPrecioSerializer,
    TendenciaMensualItemSerializer,
)


def _parse_date(value: str, param: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError:
        raise ValueError(f"'{param}' debe tener formato YYYY-MM-DD.")


def _require_date_range(
    params: dict,
) -> tuple[date, date] | tuple[None, None]:
    errors: dict[str, str] = {}
    parsed: dict[str, date] = {}

    for key in ("fecha_inicio", "fecha_fin"):
        val = params.get(key)
        if not val:
            errors[key] = f"El parámetro '{key}' es requerido."
            continue
        try:
            parsed[key] = _parse_date(val, key)
        except ValueError as exc:
            errors[key] = str(exc)

    if errors:
        raise ValidationError(errors)

    if parsed["fecha_inicio"] > parsed["fecha_fin"]:
        raise ValidationError(
            {"detail": "fecha_inicio no puede ser posterior a fecha_fin."}
        )

    return parsed["fecha_inicio"], parsed["fecha_fin"]


class HistorialPrecioViewSet(viewsets.ModelViewSet):
    serializer_class = HistorialPrecioSerializer
    queryset = HistorialPrecio.objects.all()

    def get_queryset(self):
        qs = HistorialPrecio.objects.all()
        params = self.request.query_params
        errors: dict[str, str] = {}
        parsed: dict[str, date] = {}

        for key in ("fecha_inicio", "fecha_fin"):
            val = params.get(key)
            if not val:
                continue
            try:
                parsed[key] = _parse_date(val, key)
            except ValueError as exc:
                errors[key] = str(exc)

        if errors:
            raise ValidationError(errors)

        inicio = parsed.get("fecha_inicio")
        fin = parsed.get("fecha_fin")

        if inicio and fin and inicio > fin:
            raise ValidationError(
                {"detail": "fecha_inicio no puede ser posterior a fecha_fin."}
            )

        if inicio:
            qs = qs.filter(fecha__gte=inicio)
        if fin:
            qs = qs.filter(fecha__lte=fin)

        return qs

    @action(detail=False, methods=["get"])
    def actual(self, request: Request) -> Response:
        precio = services.precio_actual()
        if precio is None:
            return Response(
                {"detail": "Sin registros de precios."}, status=status.HTTP_404_NOT_FOUND
            )
        return Response(HistorialPrecioSerializer(precio).data)

    @action(detail=False, methods=["get"])
    def estadisticas(self, request: Request) -> Response:
        fecha_inicio, fecha_fin = _require_date_range(request.query_params)
        data = services.estadisticas(fecha_inicio, fecha_fin)
        return Response(EstadisticasSerializer(data).data)

    @action(detail=False, methods=["get"])
    def tendencia(self, request: Request) -> Response:
        anio_str = request.query_params.get("anio")
        if not anio_str:
            return Response(
                {"detail": "El parámetro 'anio' es requerido."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            anio = int(anio_str)
            if not (2000 <= anio <= 2100):
                raise ValueError
        except ValueError:
            return Response(
                {"detail": "El parámetro 'anio' debe ser un año válido (ej. 2026)."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = services.tendencia_mensual(anio)
        return Response(TendenciaMensualItemSerializer(data, many=True).data)

    @action(detail=False, methods=["get"])
    def comparar(self, request: Request) -> Response:
        params = request.query_params
        errors: dict[str, str] = {}
        parsed: dict[str, date] = {}

        for key in ("p1_inicio", "p1_fin", "p2_inicio", "p2_fin"):
            val = params.get(key)
            if not val:
                errors[key] = f"El parámetro '{key}' es requerido."
                continue
            try:
                parsed[key] = _parse_date(val, key)
            except ValueError as exc:
                errors[key] = str(exc)

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        if parsed["p1_inicio"] > parsed["p1_fin"]:
            return Response(
                {"detail": "p1_inicio no puede ser posterior a p1_fin."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if parsed["p2_inicio"] > parsed["p2_fin"]:
            return Response(
                {"detail": "p2_inicio no puede ser posterior a p2_fin."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = services.comparar_periodos(
            parsed["p1_inicio"], parsed["p1_fin"],
            parsed["p2_inicio"], parsed["p2_fin"],
        )
        return Response(ComparacionPeriodosSerializer(data).data)
