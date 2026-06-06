from django.db import models


class Parcela(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    area_hectareas = models.DecimalField(max_digits=8, decimal_places=2)
    activa = models.BooleanField(default=True)
    notas = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "parcela"
        verbose_name_plural = "parcelas"
        ordering = ["nombre"]

    def __str__(self) -> str:
        return self.nombre
