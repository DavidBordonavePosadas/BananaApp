from django.contrib import admin

from .models import Cosecha


@admin.register(Cosecha)
class CosechaAdmin(admin.ModelAdmin):
    list_display = ["fecha", "parcela", "peso_kg", "precio_kg", "creado_por"]
    list_filter = ["parcela", "fecha"]
    date_hierarchy = "fecha"
