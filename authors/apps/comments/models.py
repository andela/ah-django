from django.db import models
from ..articles.models import Articles
from ..authentication.models import User
from simple_history.models import HistoricalRecords


class Comments(models.Model):
    """Articles comment model
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    body = models.TextField()
    article = models.ForeignKey(Articles, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    highlighted_text = models.TextField(null=True)
    comment_history = HistoricalRecords()
