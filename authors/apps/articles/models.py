from django.db import models
from django.contrib.postgres.fields import ArrayField
from ..authentication.models import User


class Article(models.Model):
    """Article model"""
    title = models.CharField(max_length=100, blank=False)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=False)
    body = models.TextField(blank=False)
    tagList = ArrayField(
        models.CharField(max_length=100, blank=False)
    )
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(blank=True, null=True, auto_now=True)
    # author = models.CharField(max_length=100, blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
