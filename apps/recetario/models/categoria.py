from uuid import uuid4
from django.db import models


class Categoria(models.Model):
    u"""Categoria
        |id: identificador (uuid)
        |nombre: nombre, ejm: abarrotes, cereales, etc.
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    nombre = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.nombre
