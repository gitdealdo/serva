from uuid import uuid4
from django.db import models

from .producto import Producto
from .receta import Receta


class Ingrediente(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    producto = models.ForeignKey(Producto)
    cantidad = models.DecimalField(max_digits=9, decimal_places=2)
    receta = models.ForeignKey(
        Receta, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name = "Ingrediente"
        verbose_name_plural = "Ingredientes"

    def __str__(self):
        return self.producto.nombre
