""" This module defines the models for highlights """

from django.db import models
from authors import settings
from authors.apps.articles.models import Article


User = settings.AUTH_USER_MODEL


class Highlight(models.Model):
    """
    This class defines models for highlights
    """
    highlighter = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, blank=True, null=True)
    highlight = models.CharField(
        max_length=1000, blank=True, null=True)
    comment = models.CharField(
        max_length=200, blank=True, null=True)
