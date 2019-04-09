from django.db import models
from django.db.models.signals import post_save

from authors.apps.articles.models import Article
from authors.apps.authentication.models import User
from authors.apps.notifications.signals import commented_on
from django.contrib.contenttypes.fields import GenericRelation

from authors.apps.reactions.models import UserReaction


class Comment(models.Model):
    """
        Comments model
    """
    body = models.TextField(blank=False, db_index=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='author')
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='article')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_reaction = GenericRelation(UserReaction, related_query_name='comment')

    def __repr__(self):
        return self.body

    class Meta:
        order_with_respect_to = 'article'
        unique_together = ('body', 'article', 'author')

    @property
    def replies(self):
        """
            Gives replies made to a comment
        """
        queryset = CommentReply.objects.filter(
            comment_to__body=self.body).values()
        return [item.get('body') for item in list(queryset)]


class CommentReply(models.Model):
    """
        Models the comments reply
    """

    body = models.TextField(blank=False, db_index=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    comment_to = models.ForeignKey(Comment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created_at',)
        unique_together = ('body', 'comment_to', 'author')


post_save.connect(commented_on, sender=Comment)
