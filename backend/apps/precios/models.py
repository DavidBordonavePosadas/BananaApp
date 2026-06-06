from django.db import models


class HistorialPrecio(models.Model):
    fecha = models.DateField(unique=True)
    precio_kg = models.DecimalField(max_digits=8, decimal_places=2)
    notas = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "historial de precio"
        verbose_name_plural = "historial de precios"
        ordering = ["-fecha"]

    def __str__(self) -> str:
        return f"{self.fecha}: ${self.precio_kg}/kg"
