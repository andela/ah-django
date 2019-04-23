from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from asgiref.sync import async_to_sync
from authors.consumers import send_notification
from authors.apps.profiles.models import Follow
from authors.apps.articles.models import (Favorites)


def send_email_messages(users, subject, message, link):
    """
        send an email notification to the list of users
    """

    message = render_to_string(
        'newinteraction.html', {
            'message': message,
            'link': link
        })
    from_email = settings.FROM_EMAIL

    send_mail(
        subject,
        message,
        from_email, [user.email for user in users],
        html_message=message,
        fail_silently=False)


def send_socket_message(users, message):
    """
        send notifications via websockets to the
        list of users present
    """
    notification = {
        'send_to': [user.username for user in users],
        'message': message}
    async_to_sync(send_notification)(notification)


def author_followers(author):
    """
        this function is meant to return the followers of
        the author
    """
    all_followers = Follow.objects.filter(following=author)
    in_app_authorizers = [
        n.user for n in all_followers if n.user.in_app_notifications]
    email_notifications_authorizers = [
        n.user for n in all_followers if n.user.email_notifications]
    return (in_app_authorizers, email_notifications_authorizers)


def get_article_favoriters(article):
    """
    get all those that had favorited an article
    """
    all_favoriters = [n.user for n in Favorites.objects.filter(
        article=article)]
    in_app_authorizers = [
        n for n in all_favoriters if n.in_app_notifications]
    email_authorizers = [
        n for n in all_favoriters if n.email_notifications]

    return (in_app_authorizers, email_authorizers)
