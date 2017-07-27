from uuid import uuid4
from django.db import models

from backend_apps.auths.models import User
from apps.recetario.models.receta import Receta

from .menu import Menu


class Detalle(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    menu = models.ForeignKey(Menu, verbose_name=u"Menu",)
    receta = models.ForeignKey(Receta)
    porcion = models.IntegerField(u"Porción")
    user = models.ForeignKey(User)

    class Meta:
        verbose_name = "Detalle"
        verbose_name_plural = "Detalles"

    def __str__(self):
        return "detalle"
