from uuid import uuid4
from django.db import models


class Tipo(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    nombre = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Tipo"
        verbose_name_plural = "Tipos"

    def __str__(self):
        return self.nombre
