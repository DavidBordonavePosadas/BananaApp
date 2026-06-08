from django.contrib import admin

from .models import CompraInsumo, TipoInsumo


@admin.register(TipoInsumo)
class TipoInsumoAdmin(admin.ModelAdmin):
    list_display = ["nombre", "activo"]
    list_filter = ["activo"]


@admin.register(CompraInsumo)
class CompraInsumoAdmin(admin.ModelAdmin):
    list_display = ["fecha", "tipo_insumo", "costo", "proveedor", "creado_por"]
    list_filter = ["tipo_insumo"]
    date_hierarchy = "fecha"
