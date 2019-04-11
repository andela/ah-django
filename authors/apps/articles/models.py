from django.db import models
from authors.apps.authentication.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.postgres.fields import ArrayField

from authors.apps.utils.slug_generator import Slug

from datetime import datetime


class Articles(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    body = models.TextField()
    image_url = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               to_field='username')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200, unique=True)
    tags = ArrayField(models.CharField(max_length=20), default=list)
    # favorited = models.BooleanField(default=False)
    # favoritesCount = models.IntegerField(default=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_title = self.title
        self.old_description = self.description
        self.old_body = self.body
        self.old_image = self.image_url

        self.old_fields = [self.old_title,
                           self.old_description,
                           self.old_body,
                           self.old_image]

        self.fields = [
            self.title,
            self.description,
            self.body,
            self.image_url
        ]

    def save(self, *args, **kwargs):
        """ overrides the save method
            generates a new slug in none exists
            updates the time a field was updated
        """
        if not self.id:
            self.slug = Slug().generate_unique_slug(Articles, self.title)

        for fields in self.fields:
            if self.old_fields != self.fields and self.fields:
                self.updated_at = datetime.now()
        super().save(*args, **kwargs)


class Rating(models.Model):
    article_id = models.ForeignKey(Articles, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MaxValueValidator(5),
                                             MinValueValidator(0)])


class LikesManager(models.Manager):
    """Extend the default manager to help get likes and dislikes
    """

    def likes(self):
        return self.get_queryset().filter(like=1)

    def dislikes(self):
        return self.get_queryset().filter(like=-1)


class Likes(models.Model):
    """Like model for the app
    """
    article = models.ForeignKey(Articles, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = LikesManager()

    class Meta:
        unique_together = (("article", "user"),)


class Comments(models.Model):
    article_slug = models.SlugField(max_length=200)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    body = models.TextField()
    author = models.CharField(max_length=200)


class Favorites(models.Model):
    """ Favorites model for the app"""

    article = models.ForeignKey(Articles, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
