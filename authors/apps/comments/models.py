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


class LikeManager(models.Manager):
    """
    Used to return likes and dislikes for a
    specific comment
    """

    def likes(self):
        return self.get_queryset().filter(like=1)

    def dislikes(self):
        return self.get_queryset().filter(like=-1)


class Like(models.Model):
    """
    Like dislike comment model
    """
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = LikeManager()

    class Meta:
        unique_together = (("comment", "user"),)
    