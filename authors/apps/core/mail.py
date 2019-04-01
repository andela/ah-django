"""
    This module holds the appllcation's emailing helper functions
"""
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives, send_mail as _send_mail

import os


class Mail:
    """
        Handles sending of emails

        Parameters:
        ---------
        sender_addr: str
            Preferred email host address
    """

    def __init__(self, sender_addr=None):
        self._sender_email = sender_addr
        self.current_site = None

    def __call__(self, request):
        """
            request: Werkzeug request context
            The current request context
        """
        self.current_site = get_current_site(
            request)

    def __set_sender_email(self, addr):
        """
            Sets the host email address to be used in
            sending mails
        """
        if not addr:
            addr = os.environ.get('EMAIL_HOST_USER')
        return addr

    @property
    def sender_email(self):
        return self._sender_email

    @sender_email.setter
    def sender_email(self, email_addr):
        self._sender_email = self.__set_sender_email(email_addr)

    def send_mail(self, subject, message=None,
                  to_addrs=[], multiple_alternatives=False, template_name=None,
                  template_values={}):
        """
            Sends an email using the specified addresses

            Parameters:
            ----------
            subject: str
                Email subject
            to_addrs: list
                Email receipients
            message: str
                Email body (for a plain/text email format)
            multiple_alternatives: boolean
                Send email in text/html format
                If false, email is sent as plain text
            template_name: str
                The path to the HTML template to send email in
                Requires multiple alternatives set to True
            template_values: dict
                key: pair items to render in the template message
        """

        if multiple_alternatives:
            template = render_to_string(template_name, template_values)
            body_msg = strip_tags(template)

            email = EmailMultiAlternatives(
                subject, body_msg, self.sender_email, to_addrs)
            email.attach_alternative(template, 'text/html')
            email.send()

        elif not multiple_alternatives:
            _send_mail(subject, message, to_addrs)

    def get_link(self, domain=None, path='', token=''):
        """
            Creates and returns a http link from the given domain
            and path
             -> A call to the instance with the request argument
                can be used to generate the domain
                  e.g mail_instance(request)
        """

        if not domain:
            domain = self.current_site.domain

        return f'http://{domain}/{path}/{token}/'


mail_helper = Mail()
