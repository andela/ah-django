from django.db import models
from authors.apps.authentication.models import User
from authors.apps.articles.models import Articles


class ReportArticle(models.Model):
    """ Report article model """

    article = models.ForeignKey(Articles, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    report = models.TextField()
    viewed = models.BooleanField(default=False)
    action_taken = models.CharField(default="Pending", max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
