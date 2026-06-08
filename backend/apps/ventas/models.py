from decimal import Decimal

from django.db import models


class Venta(models.Model):
    cliente = models.ForeignKey(
        "clientes.Cliente", on_delete=models.PROTECT, related_name="ventas"
    )
    fecha = models.DateField()
    peso_kg = models.DecimalField(max_digits=10, decimal_places=2)
    precio_kg = models.DecimalField(max_digits=8, decimal_places=2)
    notas = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "venta"
        verbose_name_plural = "ventas"
        ordering = ["-fecha"]

    def __str__(self) -> str:
        return f"Venta {self.fecha} — {self.cliente}"

    @property
    def total(self) -> Decimal:
        return self.peso_kg * self.precio_kg
