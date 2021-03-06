from uuid import uuid4
from django.db import models

from .producto import Producto
from .receta import Receta


class Ingrediente(models.Model):
    u"""Ingrediente
        |id: identificador (uuid)
        |producto: id del producto/insumo
        |cantidad: cantidad del insumo
        |receta: a la que pertenece este insumo
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    producto = models.ForeignKey(Producto)
    cantidad = models.DecimalField(max_digits=9, decimal_places=2)
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Ingrediente"
        verbose_name_plural = "Ingredientes"

    def __str__(self):
        return self.producto.nombre
