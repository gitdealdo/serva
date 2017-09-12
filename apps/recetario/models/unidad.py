from uuid import uuid4
from django.db import models


class Unidad(models.Model):
    u"""Unidad
        |id: identificador (uuid)
        |nombre: nombre
        |simbolo: simbolo
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    nombre = models.CharField(max_length=30)
    simbolo = models.CharField(u"Símbolo", max_length=10, default="Und")

    class Meta:
        verbose_name = "Unidad"
        verbose_name_plural = "Unidades"

    def __str__(self):
        return self.nombre
