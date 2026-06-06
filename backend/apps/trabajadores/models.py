from django.db import models


class Trabajador(models.Model):
    nombre = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20, blank=True)
    activo = models.BooleanField(default=True)
    notas = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "trabajador"
        verbose_name_plural = "trabajadores"
        ordering = ["nombre"]

    def __str__(self) -> str:
        return self.nombre


class Actividad(models.Model):
    nombre = models.CharField(max_length=200, unique=True)

    class Meta:
        verbose_name = "actividad"
        verbose_name_plural = "actividades"
        ordering = ["nombre"]

    def __str__(self) -> str:
        return self.nombre


class RegistroTrabajo(models.Model):
    trabajador = models.ForeignKey(
        Trabajador, on_delete=models.PROTECT, related_name="registros"
    )
    parcela = models.ForeignKey(
        "parcelas.Parcela",
        on_delete=models.SET_NULL,
        null=True,
        related_name="registros_trabajo",
    )
    actividad = models.ForeignKey(
        Actividad, on_delete=models.PROTECT, related_name="registros"
    )
    fecha = models.DateField()
    pago = models.DecimalField(max_digits=10, decimal_places=2)
    notas = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "registro de trabajo"
        verbose_name_plural = "registros de trabajo"
        ordering = ["-fecha"]

    def __str__(self) -> str:
        return f"{self.trabajador} — {self.actividad} — {self.fecha}"
