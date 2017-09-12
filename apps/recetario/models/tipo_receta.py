from uuid import uuid4
from django.db import models


class TipoReceta(models.Model):
    u"""TipoReceta
        |id: identificador (uuid)
        |nombre: ejm: entrada, principal, postre, etc
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    nombre = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Tipo Receta"
        verbose_name_plural = "Tipo Recetas"

    def __str__(self):
        return self.nombre
