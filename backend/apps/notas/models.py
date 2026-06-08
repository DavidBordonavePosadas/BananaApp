from django.conf import settings
from django.db import models


class Nota(models.Model):
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="notas"
    )
    fecha = models.DateField()
    titulo = models.CharField(max_length=200, blank=True)
    contenido = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "nota"
        verbose_name_plural = "notas"
        ordering = ["-fecha"]

    def __str__(self) -> str:
        return self.titulo or f"Nota {self.fecha}"
