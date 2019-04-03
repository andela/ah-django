"""
    This test module holds tests related to sending of mails
"""
from rest_framework import status
from django.contrib.sites.shortcuts import get_current_site
from django.core import mail

from .base_test import BaseTestCase


class TestMail(BaseTestCase):
    """
        Holds mail-related tests
    """

    def test_email_is_sent_on_user_registration(self):
        """
            A user should receive an  activation request email
            upon successful registration.
        """
        success_msg = 'sent'
        outbox_count = len(mail.outbox)

        with self.settings(
                EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
            res = self.register_new_user(data=self.user_to_register)
        outbox = mail.outbox[0]
        print(res)

        self.assertIn(success_msg, res.data.get('message'))
        self.assertEqual(outbox.subject, 'Activate Account')
        self.assertTrue(len(mail.outbox) == outbox_count + 1)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_user_recives_activation_link_in_email(self):
        """
            The sent 'registration' email should enable the user
            to verify their account
        """

        # Clear outbox
        mail.outbox = []

        request_ctx = self.factory.post(self.registration_path,
                                        self.user_to_register,
                                        format='json')
        with self.settings(
                EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
            respose = self.register_new_user(data=self.user_to_register)
        site = get_current_site(request_ctx).domain
        append_ = respose.data.get('token', '')
        verification_url = f"http://{site}/activate/{append_}"

        self.assertIn(verification_url, mail.outbox[0].body)
