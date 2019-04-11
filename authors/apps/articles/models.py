""" This module defines models for articles """

from django.db.models.signals import post_save
from authors.apps.reactions.models import UserReaction
from authors.apps.authentication.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.fields import ArrayField
from django.db import models
from authors.apps.notifications.signals import article_created


class Article(models.Model):
    """Article model"""
    title = models.CharField(max_length=100, blank=False)
    slug = models.SlugField(unique=True, db_index=True)
    description = models.TextField(blank=False)
    body = models.TextField(blank=False)
    tagList = ArrayField(
        models.CharField(max_length=100), blank=True, null=True
    )
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(blank=True, null=True, auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    user_reaction = GenericRelation(UserReaction, related_query_name='article')
    reading_time = models.CharField(blank=True, null=True, max_length=100)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.title


class ArticleRating(models.Model):
    """Ratings model"""
    rater = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    rating = models.IntegerField()


post_save.connect(article_created, sender=Article)
