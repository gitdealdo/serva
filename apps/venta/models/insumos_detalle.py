"""app:venta"""
from uuid import uuid4
from django.db import models
from apps.recetario.models.producto import Producto
from .detalle import Detalle


class InsumosDetalle(models.Model):
    u"""InsumosDetalle
        |id: identificador (uuid)
        |detalle: (id) detalle del menu
        |insumo: (id) productos
        |cantidad: cantidad
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    detalle = models.ForeignKey(Detalle, on_delete=models.CASCADE)
    insumo = models.ForeignKey(Producto)
    cantidad = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)

    class Meta:
        verbose_name = "InsumosDetalle"
        verbose_name_plural = "InsumosDetalles"

    def __str__(self):
        return "detalle"
