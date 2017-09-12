from uuid import uuid4
from django.db import models

from apps.recetario.models.receta import Receta

from .menu import Menu


class Detalle(models.Model):
    u"""Detalle
        |id: identificador (uuid)
        |menu: (id) menu por fecha
        |receta: (id) recetas
        |porcion: cantidad de platos a ser preparados
        |costo: costo del menu/cantidad, no obligatorio
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    menu = models.ForeignKey(Menu, verbose_name=u"Menu",)
    receta = models.ForeignKey(Receta)
    porcion = models.IntegerField(u"Porción")
    costo = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)

    class Meta:
        verbose_name = "Detalle"
        verbose_name_plural = "Detalles"

    def __str__(self):
        return "detalle"
