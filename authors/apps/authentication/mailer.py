import sendgrid
import os
from sendgrid.helpers.mail import Email, Content, Mail

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site

from djoser.conf import settings as dj_settings


class RecoverPassword:

    def __init__(self, request=None,
                 context=None, email=None, data=None):
        self.request = request
        self.context = {}
        self.email = email
        self.user = data['user']
        self.uid = data['uid']
        self.token = data['token']

    def get_context_data(self):
        ctx = {}
        context = dict(ctx, **self.context)

        if self.request:
            site = get_current_site(self.request)
            domain = context.get('domain') or (getattr(settings, 'DOMAIN', '')
                                               or site.domain)
            protocol = context.get('protocol') or ('https'
                                                   if self.request.is_secure()
                                                   else 'http')
        else:
            domain = context.get('domain') or getattr(settings, 'DOMAIN', '')
            protocol = context.get('protocol') or 'http'

        context.update({
            'domain': domain,
            'protocol': protocol,
            'user': self.user,
            'uid': self.uid,
            'token': self.token
        })
        return context

    def send_email(self):

        sg = sendgrid.SendGridAPIClient(
            api_key=os.environ.get('SENDGRID_API_KEY'))
        from_email = Email(settings.FROM_EMAIL)
        to_email = Email(self.email)
        context = self.get_context_data()
        message = dj_settings.PASSWORD_RESET_CONFIRM_URL.format(**context)
        subject = "Reset password {}".format(context['user'])
        content = Content(
            "text/plain", message)
        mail = Mail(from_email, subject, to_email, content)
        response = sg.client.mail.send.post(request_body=mail.get())
        return response
