from django.db import models
from ..authentication.models import User
from authors.apps.articles.models import Article


class BookmarkArticle(models.Model):
    """ User Bookmark holder class """
    class Meta:
        unique_together = ('_article', 'user')

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='user',
        related_name='user'
    )

    _article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        verbose_name='_article',
        related_name='_article'
    )

    def __str__(self):
        """ Return title of bookmarked article """
        return self._article.slug
