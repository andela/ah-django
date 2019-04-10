from django.core.mail import send_mail
from django.conf import settings


class Email:
    """
    Class for sending an email
    """

    def __init__(self, subject, message, to_email):
        self.subject = subject
        self.message = message
        self.to_email = to_email
        self.from_email = settings.FROM_EMAIL

    def send(self):
        send_mail(self.subject, self.message, self.from_email,
                  self.to_email, fail_silently=False)
