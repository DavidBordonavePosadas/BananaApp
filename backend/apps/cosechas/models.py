from django.conf import settings
from django.db import models


class Cosecha(models.Model):
    parcela = models.ForeignKey(
        "parcelas.Parcela", on_delete=models.PROTECT, related_name="cosechas"
    )
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="cosechas"
    )
    fecha = models.DateField()
    racimos_cortados = models.PositiveIntegerField()
    rejas_producidas = models.PositiveIntegerField()
    peso_kg = models.DecimalField(max_digits=10, decimal_places=2)
    precio_kg = models.DecimalField(max_digits=8, decimal_places=2)
    notas = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "cosecha"
        verbose_name_plural = "cosechas"
        ordering = ["-fecha"]

    def __str__(self) -> str:
        return f"Cosecha {self.fecha} — {self.parcela}"

    @property
    def total_estimado(self) -> float:
        return float(self.peso_kg * self.precio_kg)
