from django.db import models

from apps.blog.models.post import Post


class Comment(models.Model):
    u"""Post Model."""

    post = models.ForeignKey(Post)
    body = models.TextField()

    created_at = models.DateTimeField(u'created at', auto_now_add=True)
    updated_at = models.DateTimeField(u'updated at', auto_now=True)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Commnets"

    def __str__(self):
        return self.title
