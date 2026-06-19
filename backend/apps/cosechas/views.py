from datetime import date

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import services
from .models import Cosecha
from .serializers import (
    CosechaSerializer,
    ProduccionMensualSerializer,
    ProduccionPorParcelaSerializer,
    ProduccionSemanalSerializer,
    ResumenPeriodoSerializer,
)


def _parse_date(value: str, field_name: str) -> tuple[date | None, str | None]:
    try:
        return date.fromisoformat(value), None
    except (ValueError, TypeError):
        return None, f"{field_name}: formato inválido, use YYYY-MM-DD."


class CosechaViewSet(viewsets.ModelViewSet):
    serializer_class = CosechaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Cosecha.objects.select_related("parcela", "creado_por").order_by("-fecha")
        params = self.request.query_params
        if parcela_id := params.get("parcela"):
            qs = qs.filter(parcela_id=parcela_id)
        if fecha_inicio := params.get("fecha_inicio"):
            qs = qs.filter(fecha__gte=fecha_inicio)
        if fecha_fin := params.get("fecha_fin"):
            qs = qs.filter(fecha__lte=fecha_fin)
        return qs

    def perform_create(self, serializer: CosechaSerializer) -> None:
        serializer.save(creado_por=self.request.user)

    def _require_dates(
        self, request
    ) -> tuple[date | None, date | None, Response | None]:
        fecha_inicio_raw = request.query_params.get("fecha_inicio")
        fecha_fin_raw = request.query_params.get("fecha_fin")
        if not fecha_inicio_raw or not fecha_fin_raw:
            return None, None, Response(
                {"error": "fecha_inicio y fecha_fin son requeridos."}, status=400
            )
        fecha_inicio, err = _parse_date(fecha_inicio_raw, "fecha_inicio")
        if err:
            return None, None, Response({"error": err}, status=400)
        fecha_fin, err = _parse_date(fecha_fin_raw, "fecha_fin")
        if err:
            return None, None, Response({"error": err}, status=400)
        if fecha_fin < fecha_inicio:
            return None, None, Response(
                {"error": "fecha_fin debe ser mayor o igual a fecha_inicio."}, status=400
            )
        return fecha_inicio, fecha_fin, None

    @action(detail=False, methods=["get"], url_path="por-parcela")
    def por_parcela(self, request):
        fecha_inicio, fecha_fin, error = self._require_dates(request)
        if error:
            return error
        data = services.produccion_por_parcela(fecha_inicio, fecha_fin)
        return Response(ProduccionPorParcelaSerializer(data, many=True).data)

    @action(detail=False, methods=["get"], url_path="mensual")
    def mensual(self, request):
        anio_raw = request.query_params.get("anio")
        if not anio_raw:
            return Response({"error": "anio es requerido."}, status=400)
        try:
            anio = int(anio_raw)
            if anio < 2000 or anio > 2100:
                raise ValueError
        except ValueError:
            return Response({"error": "anio: valor inválido."}, status=400)
        data = services.produccion_mensual(anio)
        return Response(ProduccionMensualSerializer(data, many=True).data)

    @action(detail=False, methods=["get"], url_path="semanal")
    def semanal(self, request):
        fecha_inicio, fecha_fin, error = self._require_dates(request)
        if error:
            return error
        data = services.produccion_semanal(fecha_inicio, fecha_fin)
        return Response(ProduccionSemanalSerializer(data, many=True).data)

    @action(detail=False, methods=["get"], url_path="resumen")
    def resumen(self, request):
        fecha_inicio, fecha_fin, error = self._require_dates(request)
        if error:
            return error
        data = services.resumen_periodo(fecha_inicio, fecha_fin)
        return Response(ResumenPeriodoSerializer(data).data)
