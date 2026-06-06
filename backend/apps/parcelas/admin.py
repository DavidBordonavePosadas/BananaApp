from django.contrib import admin

from .models import Parcela


@admin.register(Parcela)
class ParcelaAdmin(admin.ModelAdmin):
    list_display = ["nombre", "area_hectareas", "activa", "created_at"]
    list_filter = ["activa"]
    search_fields = ["nombre"]
