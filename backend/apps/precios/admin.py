from django.contrib import admin

from .models import HistorialPrecio


@admin.register(HistorialPrecio)
class HistorialPrecioAdmin(admin.ModelAdmin):
    list_display = ["fecha", "precio_kg", "created_at"]
    date_hierarchy = "fecha"
