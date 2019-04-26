"""
This module defines models for the profile
"""
from django.db import models
from cloudinary.models import CloudinaryField
from django.conf import settings
from django.db.models.signals import post_save


class Profile(models.Model):
    """
    Define models for user profile
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    first_name = models.CharField(max_length=40, blank=True, null=True)
    last_name = models.CharField(max_length=40, blank=True, null=True)
    country = models.CharField(max_length=40, blank=True, null=True)
    phone_number = models.IntegerField(default=0, blank=True, null=True)
    bio = models.CharField(max_length=250, blank=True, null=True)
    birth_day = models.DateField(blank=True, null=True)
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)
    image = CloudinaryField(
        "image",
        default='https://res.cloudinary.com/wekesa931/' +
                'image/upload/v1554520694/samples/bike.jpg')

    def __str__(self):
        return self.user.username


def create_profile(instance, created, **kwargs):
    """
    Creates the user profile
    """

    if created:
        profile = Profile(user=instance)
        profile.save()


post_save.connect(create_profile, sender=settings.AUTH_USER_MODEL)
