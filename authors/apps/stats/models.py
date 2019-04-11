from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from authors.apps.authentication.models import User


class ReadStats(models.Model):
    """
        Users read statistics
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_index=True)
    reads = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)


@receiver(post_save, sender=User)
def create_user_stats(sender, instance, created, **kwargs):
    """
        Creates the user statistics on save of the user
        model
    """

    if created:
        ReadStats.objects.create(user=instance)
