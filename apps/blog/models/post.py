from uuid import uuid4

from django.db import models

from backend_apps.auths.models import User


class Post(models.Model):
    u"""Post Model."""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=10, verbose_name=u'Título')
    body = models.TextField()
    state = models.BooleanField(default=True)
    user = models.ForeignKey(User)

    created_at = models.DateTimeField(u'created at', auto_now_add=True)
    updated_at = models.DateTimeField(u'updated at', auto_now=True)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return self.title
