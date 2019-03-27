"""
    This test module holds tests related to sending of mails
"""
from rest_framework import status
from django.contrib.sites.shortcuts import get_current_site
from django.core import mail

from .base_test import BaseTestCase


class TestMail(BaseTestCase):
    """
        Holds user account tests
    """

    def test_email_is_sent_on_user_request_to_reset_password(self):
        """
            A user should receive an activation email after 
            requesting to reset password
        """
        pass

    def test_user_receives_email_reset_link(self):
        """
           A usershould receive a reset link on request
        """
        pass