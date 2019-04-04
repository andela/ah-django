from .base_test import BaseTestCase
from rest_framework.views import status


class TestSocialLogin(BaseTestCase):
    """
    Thes the social authentication endpoint
    """

    def test_google_auth(self):
        response = self.client.post(
            self.social_auth_path,
            self.google_social_auth,
            format="json"
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_facebook_auth_failure(self):
        response = self.client.post(
            self.social_auth_path,
            self.facebook_social_wrong_auth,
            format="json"
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_twitter_auth(self):
        response = self.client.post(
            self.social_auth_path,
            self.twitter_social_auth,
            format="json"
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_facebook_auth_success(self):
        response = self.client.post(
            self.social_auth_path,
            self.facebook_social_auth,
            format="json"
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
