from django.db import models

from django.contrib.auth.models import User


class Article(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()

    def __str__(self):
        return f"{self.title}"
