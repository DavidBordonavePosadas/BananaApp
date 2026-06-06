from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    class Rol(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        OPERADOR = "OPERADOR", "Operador"

    rol = models.CharField(max_length=10, choices=Rol.choices, default=Rol.OPERADOR)

    class Meta:
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"
