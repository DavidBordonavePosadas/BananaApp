from django.contrib import admin

from .models import Venta


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ["fecha", "cliente", "peso_kg", "precio_kg", "monto_pagado"]
    list_filter = ["cliente"]
    date_hierarchy = "fecha"
