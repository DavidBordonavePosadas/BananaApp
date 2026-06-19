from datetime import date

from django.db.models import Count, DecimalField, ExpressionWrapper, F, Sum
from django.db.models.functions import ExtractMonth, TruncWeek

from .models import Cosecha

_valor_expr = ExpressionWrapper(
    F("peso_kg") * F("precio_kg"),
    output_field=DecimalField(max_digits=14, decimal_places=2),
)


def produccion_por_parcela(fecha_inicio: date, fecha_fin: date) -> list[dict]:
    qs = (
        Cosecha.objects.filter(fecha__range=[fecha_inicio, fecha_fin])
        .values("parcela_id", "parcela__nombre")
        .annotate(total_peso=Sum("peso_kg"), total_valor=Sum(_valor_expr))
        .order_by("-total_peso")
    )
    return [
        {
            "parcela_id": row["parcela_id"],
            "parcela_nombre": row["parcela__nombre"],
            "total_peso": row["total_peso"],
            "total_valor": row["total_valor"],
        }
        for row in qs
    ]


def produccion_mensual(anio: int) -> list[dict]:
    datos = {
        row["mes"]: row
        for row in (
            Cosecha.objects.filter(fecha__year=anio)
            .annotate(mes=ExtractMonth("fecha"))
            .values("mes")
            .annotate(total_peso=Sum("peso_kg"), total_valor=Sum(_valor_expr))
        )
    }
    return [
        {
            "mes": mes,
            "total_peso": datos[mes]["total_peso"] if mes in datos else None,
            "total_valor": datos[mes]["total_valor"] if mes in datos else None,
        }
        for mes in range(1, 13)
    ]


def produccion_semanal(fecha_inicio: date, fecha_fin: date) -> list[dict]:
    qs = (
        Cosecha.objects.filter(fecha__range=[fecha_inicio, fecha_fin])
        .annotate(semana=TruncWeek("fecha"))
        .values("semana")
        .annotate(total_peso=Sum("peso_kg"), total_valor=Sum(_valor_expr))
        .order_by("semana")
    )
    return [
        {
            "semana": row["semana"],
            "total_peso": row["total_peso"],
            "total_valor": row["total_valor"],
        }
        for row in qs
    ]


def resumen_periodo(fecha_inicio: date, fecha_fin: date) -> dict:
    qs = Cosecha.objects.filter(fecha__range=[fecha_inicio, fecha_fin])
    totales = qs.aggregate(
        total_peso=Sum("peso_kg"),
        total_valor=Sum(_valor_expr),
        num_cosechas=Count("id"),
    )
    top_row = (
        qs.values("parcela_id", "parcela__nombre")
        .annotate(total_peso=Sum("peso_kg"))
        .order_by("-total_peso")
        .first()
    )
    top_parcela = (
        {
            "parcela_id": top_row["parcela_id"],
            "parcela_nombre": top_row["parcela__nombre"],
            "total_peso": top_row["total_peso"],
        }
        if top_row
        else None
    )
    return {
        "total_peso": totales["total_peso"],
        "total_valor": totales["total_valor"],
        "num_cosechas": totales["num_cosechas"],
        "top_parcela": top_parcela,
    }
