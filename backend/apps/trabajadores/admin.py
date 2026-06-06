from django.contrib import admin

from .models import Actividad, RegistroTrabajo, Trabajador


@admin.register(Trabajador)
class TrabajadorAdmin(admin.ModelAdmin):
    list_display = ["nombre", "telefono", "activo"]
    list_filter = ["activo"]
    search_fields = ["nombre"]


@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
    list_display = ["nombre"]
    search_fields = ["nombre"]


@admin.register(RegistroTrabajo)
class RegistroTrabajoAdmin(admin.ModelAdmin):
    list_display = ["fecha", "trabajador", "actividad", "parcela", "pago"]
    list_filter = ["actividad", "parcela"]
    date_hierarchy = "fecha"
