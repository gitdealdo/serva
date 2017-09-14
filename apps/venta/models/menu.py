from uuid import uuid4
from django.db import models

from backend_apps.auths.models import User
from .tipo_menu import TipoMenu


class Menu(models.Model):
    u"""Menu
        |id: identificador (uuid)
        |tipo_menu: (id) ejm: desayuno, almuerzo, cena
        |fecha: para el momento en que se está programando el menu
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    tipo_menu = models.ForeignKey(TipoMenu)
    fecha = models.DateTimeField()
    atendido = models.BooleanField(default=False)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Menu"
        verbose_name_plural = "Menus"

    def __str__(self):
        return self.tipo_menu.nombre
