from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from authors.apps.authentication.models import User


class UserReactionManager(models.Manager):
    """
        Manages user activity on articles.
        This manager supports these activities:
            Likes and Dislikes
    """

    def fetch_popularity_status(self, avg=False):
        """
            avg: boolen
            True: Shows the average sum of likes and dislikes
            present on an article.
            A like is 1, while a dislike is -1

            False: Returns a count of users who have liked/disliked
                    an article
        """

        if avg:
            return self.get_queryset().aggregate(
                models.Sum('user_reaction')).get('user_reaction__sum') or 0
        return self.likes.count() + self.dislikes.count()

    @property
    def likes(self):
        """
            Returns a count of all likes present on
            an article.
        """
        return self.get_queryset().filter(user_reaction__gt=0)

    @property
    def dislikes(self):
        """
            Returns a count of dislikes present on an article
        """
        return self.get_queryset().filter(user_reaction__lt=0)


class UserReaction(models.Model):

    """
        Handles reactions from users to ANY other model
        in the application e.g Article, Comment

        The reaction set includes:
         - LIKE / DISLIKE
    """
    like = 1
    dislike = -1

    reaction_set = [
        (like, 'like'),
        (dislike, 'dislike')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_reaction = models.SmallIntegerField(choices=reaction_set)

    # Content types store info about all models in our authors app
    # This will be a foreign key to a model we want to associate with
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveSmallIntegerField()

    # The instance of this particular object
    # * passing in of fields done implicitly
    content_object = GenericForeignKey(
        ct_field='content_type', fk_field='object_id')

    objects = UserReactionManager()
