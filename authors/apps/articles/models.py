from django.db import models
from authors.apps.authentication.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


from authors.apps.utils.slug_generator import Slug

from datetime import datetime


class Articles(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    body = models.TextField()
    image_url = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200, unique=True)

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
    created_at = models.DateField(auto_now_add=True)


class Rating(models.Model):
    article_id = models.ForeignKey(Articles, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MaxValueValidator(5),
                                             MinValueValidator(0)])
