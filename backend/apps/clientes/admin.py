from django.contrib import admin

from .models import Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ["nombre", "telefono", "activo"]
    list_filter = ["activo"]
    search_fields = ["nombre"]
