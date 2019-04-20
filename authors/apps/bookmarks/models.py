"""
This is a models bookmark
"""
from django.db import models


from authors.apps.articles.models import Articles

from authors.apps.authentication.models import User
# Create your models here.


class Bookmarks(models.Model):
    article = models.ForeignKey(Articles, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('article', 'user')
