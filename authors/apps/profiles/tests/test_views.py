""" This module defines the test cases for the profile submodule """

from rest_framework import status
from rest_framework_jwt import utils
from django.urls import reverse
from ...authentication.tests.base_test import BaseTestCase


class TestAuthenticatedUserViewProfiles(BaseTestCase):
    """
    This class defines testcases for
    testing listing profiles functionality
    """

    def test_profile_created_successful(self):
        """
        User profile created successfully
        """

        with self.settings(
                EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
            response = self.register_new_user(data=self.user1)
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_get_profiles_unauthorized(self):
        """
        Tests the unauthorized access
        of the profile endpoint
        """

        response = self.client.get(reverse(
            'profiles:list_profiles'))
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_get_profile_success(self):
        """ Test the successful retrieve of all the profiles """

        with self.settings(
                EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
            res = self.register_new_user(data=self.user4)
        token = res.data['data']['token']
        auth = 'Bearer {}'.format(token)
        response = self.client.get(
            reverse('profiles:list_profiles'),
            HTTP_AUTHORIZATION=auth
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_get_single_profile_success(self):
        """ Test the successful retrieve of all the profiles """

        with self.settings(
                EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
            res = self.register_new_user(data=self.user2)
        token = res.data['data']['token']
        auth = 'Bearer {}'.format(token)
        url = self.profile_url + "/yellantern/"
        response = self.client.get(
            url,
            HTTP_AUTHORIZATION=auth
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_get_single_profile_failure(self):
        """ Test the successful retrieve of all the profiles """

        payload = utils.jwt_payload_handler(self.mockuser)
        token = utils.jwt_encode_handler(payload)
        auth = 'Bearer {}'.format(token)
        url = self.profile_url + "/yellan/"
        response = self.client.get(
            url,
            HTTP_AUTHORIZATION=auth
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )
        self.assertIn(
            'User profile does not exist.',
            response.data['error']
        )

    def test_edit_profile_success(self):
        """ Test the successful retrieve of all the profiles """

        with self.settings(
                EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
            res = self.register_new_user(data=self.user3)
        token = res.data['data']['token']
        auth = 'Bearer {}'.format(token)
        url = self.profile_url + "/purple/edit/"
        response = self.client.patch(
            url,
            self.first_name,
            HTTP_AUTHORIZATION=auth
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            'wanyonyi',
            response.data['first_name']
        )

    def test_edit_profile_failure(self):
        """ Test the successful retrieve of all the profiles """

        with self.settings(
                EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
            res = self.register_new_user(data=self.user3)
        token = res.data['data']['token']
        auth = 'Bearer {}'.format(token)
        url = self.profile_url + "/yellantern/edit/"
        response = self.client.patch(
            url,
            self.first_name,
            HTTP_AUTHORIZATION=auth
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )
        self.assertEqual(
            'You don\'t have permission to edit this profile',
            response.data['message']
        )
