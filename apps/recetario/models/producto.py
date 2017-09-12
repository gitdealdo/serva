from uuid import uuid4
from django.db import models

from .categoria import Categoria
from .unidad import Unidad


class Producto(models.Model):
    u"""Producto
        |id: identificador (uuid)
        |nombre: nombre del producto
        |descripcion: breve descripcion del producto, no obligatorio
        |stock_minimo: Minimo de stock en el almacen para alertar deficiencia
        |stock: cantidad siempre actual en el almacen
        |categoria: (id) categorias ejm: cereales, abarrotes
        |unidad: (id) unidad de medida
        |costo: costo unitario
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    nombre = models.CharField(max_length=70)
    descripcion = models.TextField(u"Descripción", blank=True, null=True)
    stock_minimo = models.IntegerField(default=0)
    stock = models.IntegerField(default=0)
    categoria = models.ForeignKey(Categoria, blank=True)
    unidad = models.ForeignKey(Unidad)
    costo = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return self.nombre
