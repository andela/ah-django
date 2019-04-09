from django.urls import reverse
from rest_framework import status
from authors.apps.authentication.tests.base_test import BaseTestCase

class NotificationTestCase(BaseTestCase):
    """ Defines testcases for notifications """

    def test_unauthorized_access(self):
        """ Notififcations require authentication """
        response = self.client.get(reverse('notifications:unread-notifications'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

