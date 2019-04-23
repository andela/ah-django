from django.db.models.signals import post_save


from authors.apps.articles.models import (Articles)
from authors.apps.comments.models import Comments
from authors.apps.profiles.models import Follow

from .middleware import RequestMiddleware


from .utils import (send_email_messages,
                    send_socket_message,
                    author_followers,
                    get_article_favoriters)


def send_notifications_on_new_article_creation(sender, **kwargs):
    """
        this method will be responsible for sending
        notifications, real time notifications and also
        email notifications
    """
    if kwargs['created']:
        article = kwargs['instance']
        author = kwargs['instance'].author
        # get authors followers
        (in_app_authorizers,
         email_notifications_authorizers) = author_followers(author)
        # send in app notifications
        in_app_message = "New article from {} named {}".format(
            article.author.username, article.title)
        send_socket_message(users=in_app_authorizers,
                            message=in_app_message)
        # send email notifications
        # predefine the message
        email_message = """
            {} has created a new article, titled {}.

            To read it tap the view button""".format(
            author.username, article.title)

        # get the request object from the middleware
        # this aparently works only inside a signal function
        # hence it cannot be extracted
        request = RequestMiddleware(
            get_response=None).thread_local.current_request
        host = request.get_host()
        protocol = request.scheme
        link = protocol + '://' + host + '/api/articles/{}'
        # this method is meant to cater for sending the messages
        send_email_messages(users=email_notifications_authorizers,
                            subject="{}'s New Article".format(author.username),
                            message=email_message,
                            link=link.format(article.slug))


# send notification when new article is created to the followers of the
# article's author
post_save.connect(send_notifications_on_new_article_creation, sender=Articles)


def send_notif_on_comment_creation(sender, **kwargs):
    if kwargs['created']:
        comment = kwargs['instance']
        (in_app_authorizers, email_authorizers) = get_article_favoriters(
            article=comment.article)
        email_message = """
        A new comment has been posted by {} on the article {}.

        To view the comments kindly click on the view button
        """.format(comment.user.username, comment.article.title)
        request = RequestMiddleware(
            get_response=None).thread_local.current_request
        host = request.get_host()
        protocol = request.scheme
        link = protocol + '://' + host + '/api/articles/{}/comments'
        # send emails
        send_email_messages(
            users=email_authorizers,
            subject="A New comment has been posted by {}".format(
                comment.user.username),
            message=email_message,
            link=link.format(comment.article.slug, comment.id))
        # send in app notifications
        in_app_message = "A New comment posted by {} on article {}".format(
            comment.user.username, comment.article.title)
        send_socket_message(users=in_app_authorizers,
                            message=in_app_message)


post_save.connect(
    send_notif_on_comment_creation,
    sender=Comments)

# send a notification when a user gets a new follower


def send_notification_on_gaining_follower(sender, **kwargs):
    if kwargs['created']:
        followinstance = kwargs['instance']
        in_app_authorization = [
            n for n in [followinstance.following] if n.in_app_notifications]
        email_authorization = [
            n for n in [followinstance.following] if n.email_notifications]
        # getting the link
        request = RequestMiddleware(
            get_response=None).thread_local.current_request
        host = request.get_host()
        protocol = request.scheme
        link = protocol + '://' + host + "/api/profiles/{}/"

        message = "{} has started following you ".format(
            followinstance.user.username)

        email_message = message + \
            " Tap the view button to see {}'s profile".format(
                followinstance.user.username)
        # send emails
        send_email_messages(
            users=email_authorization,
            subject="You have a new follower",
            message=email_message,
            link=link.format(followinstance.user.username))
        # in app message
        send_socket_message(users=in_app_authorization,
                            message=message)


post_save.connect(
    send_notification_on_gaining_follower,
    sender=Follow)
