from django.urls import reverse
from rest_framework_jwt import utils
from rest_framework import status
from authors.apps.authentication.tests.base_test import BaseTestCase


class NotificationTestCase(BaseTestCase):
    """ Defines testcases for notifications """

    def test_unauthorized_access(self):
        """ Notififcations require authentication """
        response = self.client.get(
            reverse('notifications:unread-notifications'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_successful_get_unread_notification(self):
        """ Successful retrival of unread notifications """

        payload = utils.jwt_payload_handler(self.testuser)
        token = utils.jwt_encode_handler(payload)
        auth = 'Bearer {0}'.format(token)
        response = self.client.get(reverse(
            'notifications:unread-notifications'),
            HTTP_AUTHORIZATION=auth,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_successful_get_read_notification(self):
        """ Successful retrival of read notifications """

        payload = utils.jwt_payload_handler(self.testuser)
        token = utils.jwt_encode_handler(payload)
        auth = 'Bearer {0}'.format(token)
        response = self.client.get(reverse(
            'notifications:read-notifications'),
            HTTP_AUTHORIZATION=auth,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_successful_mark_notification_as_read(self):
        """ Mark unread notifications as read"""

        payload = utils.jwt_payload_handler(self.testuser)
        token = utils.jwt_encode_handler(payload)
        auth = 'Bearer {0}'.format(token)
        response = self.client.put(reverse(
            'notifications:unread-notifications'),
            HTTP_AUTHORIZATION=auth,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_successful_mark_notification_as_unread(self):
        """ Mark unread notifications as unread"""

        payload = utils.jwt_payload_handler(self.testuser)
        token = utils.jwt_encode_handler(payload)
        auth = 'Bearer {0}'.format(token)
        response = self.client.put(reverse(
            'notifications:read-notifications'),
            HTTP_AUTHORIZATION=auth,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
