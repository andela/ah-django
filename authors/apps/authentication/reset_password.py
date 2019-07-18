from django.template.loader import render_to_string

from djoser.conf import settings as dj_settings

from ..utils.mailer import Email


class RecoverPassword:

    def __init__(self, request=None,
                 context=None, email=None, data=None, host=None):
        self.request = request
        self.context = {}
        self.email = email
        self.user = data['user']
        self.uid = data['uid']
        self.token = data['token']
        self.host = host

    def get_context_data(self):
        ctx = {}
        context = dict(ctx, **self.context)

        try:
            host = self.request.META['HTTP_ORIGIN']
        except KeyError:
            host = (self.request.scheme + '://' + self.request.get_host() +
                    '/api/users')

        context.update({
            'host': host,
            'user': self.user,
            'uid': self.uid,
            'token': self.token
        })
        return context

    def send_email(self):
        to_email = [self.email]
        context = self.get_context_data()
        reset_link = dj_settings.PASSWORD_RESET_CONFIRM_URL.format(**context)

        user = context['user']
        username = user
        message = render_to_string(
            'password_reset.html', {
                'username': str(username),
                'reset_link': reset_link
            }
        )
        subject = "Reset password your Authors Haven password"
        email = Email(subject=subject, message=message, html_message=message,
                      to_email=to_email)
        email.send()
