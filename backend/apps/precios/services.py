from __future__ import annotations

from datetime import date
from decimal import Decimal

from django.db.models import Avg
from django.db.models.functions import TruncMonth

from .models import HistorialPrecio


def precio_actual() -> HistorialPrecio | None:
    return HistorialPrecio.objects.order_by("-fecha").first()


def _stats_periodo(fecha_inicio: date, fecha_fin: date) -> dict:
    qs = HistorialPrecio.objects.filter(fecha__gte=fecha_inicio, fecha__lte=fecha_fin)
    total = qs.count()
    if total == 0:
        return {"promedio": None, "maximo": None, "minimo": None, "total": 0}

    agg = qs.aggregate(promedio=Avg("precio_kg"))
    max_obj = qs.order_by("-precio_kg", "fecha").first()
    min_obj = qs.order_by("precio_kg", "fecha").first()

    return {
        "promedio": agg["promedio"],
        "maximo": {"precio_kg": max_obj.precio_kg, "fecha": max_obj.fecha},
        "minimo": {"precio_kg": min_obj.precio_kg, "fecha": min_obj.fecha},
        "total": total,
    }


def estadisticas(fecha_inicio: date, fecha_fin: date) -> dict:
    return _stats_periodo(fecha_inicio, fecha_fin)


def tendencia_mensual(anio: int) -> list[dict]:
    rows = (
        HistorialPrecio.objects.filter(fecha__year=anio)
        .annotate(mes=TruncMonth("fecha"))
        .values("mes")
        .annotate(promedio=Avg("precio_kg"))
        .order_by("mes")
    )
    data_by_month: dict[int, Decimal | None] = {row["mes"].month: row["promedio"] for row in rows}
    return [{"mes": m, "promedio": data_by_month.get(m)} for m in range(1, 13)]


def comparar_periodos(
    p1_inicio: date,
    p1_fin: date,
    p2_inicio: date,
    p2_fin: date,
) -> dict:
    p1 = _stats_periodo(p1_inicio, p1_fin)
    p2 = _stats_periodo(p2_inicio, p2_fin)

    diferencia_porcentual = None
    if p1["promedio"] is not None and p2["promedio"] is not None and p2["promedio"] != 0:
        diferencia_porcentual = (p1["promedio"] - p2["promedio"]) / p2["promedio"] * 100

    return {
        "periodo_1": p1,
        "periodo_2": p2,
        "diferencia_porcentual": diferencia_porcentual,
    }
