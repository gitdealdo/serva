from uuid import uuid4
from django.db import models

from .tipo_menu import TipoMenu


class Menu(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    tipo_menu = models.ForeignKey(TipoMenu)
    costo = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    fecha = models.DateTimeField()

    class Meta:
        verbose_name = "Menu"
        verbose_name_plural = "Menus"

    def __str__(self):
        return self.tipo_menu.nombre
