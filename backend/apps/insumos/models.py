from django.conf import settings
from django.db import models


class TipoInsumo(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "tipo de insumo"
        verbose_name_plural = "tipos de insumo"
        ordering = ["nombre"]

    def __str__(self) -> str:
        return self.nombre


class CompraInsumo(models.Model):
    tipo_insumo = models.ForeignKey(
        TipoInsumo, on_delete=models.PROTECT, related_name="compras"
    )
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="compras_insumo"
    )
    fecha = models.DateField()
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    unidad = models.CharField(max_length=20, blank=True)
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    proveedor = models.CharField(max_length=200, blank=True)
    notas = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "compra de insumo"
        verbose_name_plural = "compras de insumo"
        ordering = ["-fecha"]

    def __str__(self) -> str:
        return f"{self.tipo_insumo} — {self.fecha}"
