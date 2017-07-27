from uuid import uuid4
from django.db import models

from .categoria import Categoria
from backend_apps.auths.models import User


class Receta(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    nombre = models.CharField(max_length=50)
    categoria = models.ForeignKey(Categoria, verbose_name=u"Categoría")
    descripcion = models.TextField(u"Descripción", blank=True, null=True)
    porcion = models.IntegerField(u"Porción")
    preparacion = models.TextField(u"Preparación")
    imagen = models.ImageField(u'Imágen', upload_to='recetas', blank=True)
    costo = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    user = models.ForeignKey(User)

    class Meta:
        verbose_name = "Receta"
        verbose_name_plural = "Recetas"

    def __str__(self):
        return self.nombre
