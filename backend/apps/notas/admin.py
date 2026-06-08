from django.contrib import admin

from .models import Nota


@admin.register(Nota)
class NotaAdmin(admin.ModelAdmin):
    list_display = ["fecha", "titulo", "creado_por"]
    list_filter = ["creado_por"]
    date_hierarchy = "fecha"
