from notifications.signals import notify
from django.db import models
from django.db.models.signals import post_save

from authors.settings import AUTH_USER_MODEL
from authors.apps.authentication.models import User


class Follow(models.Model):
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='follower')
    followed_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followee')

    @staticmethod
    def is_user_already_followed(followed_user_id, user_id):
        """
        Check if user is already followed
        """
        result = Follow.objects.filter(followed_user=followed_user_id,
                                       user=user_id).exists()
        return result


def was_followed(sender, instance, created, **kwargs):
    """ Notifies the user when they are followed """

    sendr = User.objects.get(id=instance.user_id)
    followed = User.objects.get(id=instance.followed_user_id)
    if created:
        notify.send(sender=sendr, recipient=followed, verb='followed',
                    description="{} followed you.".format(sendr.username))


post_save.connect(was_followed, sender=Follow)
