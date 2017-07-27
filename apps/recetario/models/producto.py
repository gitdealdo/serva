from uuid import uuid4
from django.db import models

from .tipo import Tipo
from .unidad import Unidad


class Producto(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    nombre = models.CharField(max_length=30)
    descripcion = models.TextField(u"Descripción", blank=True, null=True)
    cantidad = models.IntegerField(default=0)
    tipo = models.ForeignKey(Tipo, blank=True)
    unidad = models.ForeignKey(Unidad)
    costo = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return self.nombre
