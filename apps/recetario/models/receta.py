from uuid import uuid4
from django.db import models

from .tipo_receta import TipoReceta
from backend_apps.auths.models import User


class Receta(models.Model):
    u"""Receta
        |id: identificador (uuid)
        |nombre: receta
        |tipo_ receta: (id) ejm: plato principal, entradas, etc
        |descripcion: breve descripcion
        |porcion: para cuantas personas es esta receta
        |preparacion: paso a paso de la receta
        |imagen: imagen de la receta
        |publicar: para colocarlos al público
        |autor: (id) autor/user
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    nombre = models.CharField(max_length=50)
    tipo_receta = models.ForeignKey(TipoReceta, verbose_name=u"Categoría")
    descripcion = models.TextField(u"Descripción", blank=True, null=True)
    porcion = models.IntegerField(u"Porción")
    preparacion = models.TextField(u"Preparación", blank=True, null=True)
    imagen = models.ImageField(u'Imágen', upload_to='recetas/', blank=True, null=True)
    publicar = models.BooleanField(default=False)
    autor = models.ForeignKey(User)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Receta"
        verbose_name_plural = "Recetas"

    def __str__(self):
        return self.nombre
