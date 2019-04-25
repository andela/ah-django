from django.db import models

from authors.apps.articles.models import Articles
from authors.apps.authentication.models import User
# Create your models here.
# article
# user
# views
# created_at
# updated_at


class ReadStats(models.Model):
    """Reading statistics model
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)
    article = models.ForeignKey(Articles, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
