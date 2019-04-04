"""
this will be the model for the profiles app.
"""
from django.db import models
from django.db.models.signals import post_save

from authors import settings


User = settings.AUTH_USER_MODEL


class Profile(models.Model):
    """
        the user profile model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default="")
    image = models.URLField(max_length=150, default="")
    firstname = models.CharField(max_length=30, default="")
    lastname = models.CharField(max_length=30, default="")
    updated_at = models.DateTimeField(auto_now=True)


def create_profile(sender, **kwargs):
    # method to create a new profile will
    # have blank fields for now
    # a user will be able to update it afterwards
    if kwargs['created']:
        user_profile = Profile.objects.create(user=kwargs['instance'])
        return user_profile


post_save.connect(create_profile, sender=User)
