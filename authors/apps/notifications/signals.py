""" This module generates notifications for different activities """
from notifications.signals import notify
from notifications.models import Notification
from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from authors.apps.followers.models import Follow
from authors.apps.authentication.models import User
from ..core.mail import mail_helper
from authors.apps.notifications.consumers import NotificationConsumer


def article_created(instance, created, **kwargs):
    """
        Generates notifications when an article is published
     """
    followers = Follow.objects.filter(followed_user=instance.author.id)
    recipients = [User.objects.filter(id=follower.user_id)
                  for follower in followers]
    for recipient in recipients:
        if created:
            notify.send(sender=instance.author,
                        verb='article_created',
                        description="{} published a new article in {}".format(
                            instance.author.username, instance.tagList),
                        recipient=recipient)


def commented_on(instance, created, **kwargs):
    """
        Generates notifications on comment activity
    """
    if created:
        notify.send(sender=instance.author,
                    recipient=instance.article.author,
                    verb='comment_created',
                    description="{} commented on your article '{}'".format(
                        instance.author.username, instance.article.title
                    ))


def send_to_socket(user, message):
    """
    consolidates the message to send
     """
    async_to_sync(NotificationConsumer.send_socket_notification)(
        {'send_to': [user], 'message': message})


def email_notification(instance, created, **kwargs):
    """ sends an email notification for notifications """

    user = instance.recipient
    recipients = User.objects.filter(email=user)
    deactivation_link = "link.com"

    if created:
        for recipient in recipients:

            if recipient.email_notification:

                mail_helper.send_mail(
                    subject="Author's Haven notifictions",
                    to_addrs=[recipient.email],
                    multiple_alternatives=True,
                    template_name='notifications.html',
                    template_values={
                        'username': recipient.username,
                        'optout_link': deactivation_link,
                        'description': instance.description
                    }
                )
            send_to_socket(recipient.username, instance.description)


post_save.connect(email_notification, sender=Notification)
