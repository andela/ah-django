from rest_framework import status

from authors.apps.followers.tests.base_test import FollowerBaseTest


class FollowerTestCase(FollowerBaseTest):
    """
    This test class holds test for the followers app
    """

    def test_follow_without_auth(self):
        """
        A user should be logged in in order to follow another user
        """
        response = self.client.post(self.follow_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_follow_with_auth(self):
        """
        On login a user should therefore be able to follow another user
        """
        self.authorize_user(self.user)
        with self.settings(
                EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
            self.register_user(self.user1)
        response = self.client.post(self.follow_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_follow_non_existent_user(self):
        """
        User cannot follow unexisting user
        """
        with self.settings(
                EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
            self.authorize_user(self.user)
            response = self.client.post(self.follow_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_follow_self(self):
        """
        User cannot follow themselves
        """
        with self.settings(
                EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
            self.authorize_user(self.user)
            response = self.client.post(self.follow_self_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_already_followed(self):
        """
        User cannot follow another user more than once
        """
        self.authorize_user(self.user)
        with self.settings(
                EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
            self.register_user(self.user1)
            self.client.post(self.follow_url, format='json')
            response2 = self.client.post(self.follow_url, format='json')
        self.assertEqual(response2.content,
                         b'{"detail": {"error": "user already followed"}}')
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unfollow_user_successfully(self):
        """
        User should be able to unfollow followed user
        """
        self.authorize_user(self.user)
        with self.settings(
                EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
            self.register_user(self.user1)
            self.client.post(self.follow_url, format='json')
            response = self.client.delete(self.unfollow_url,
                                          data=self.followed_user)
        self.assertEqual(response.content,
                         b'{"message":"user unfollowed"}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unfollow_user_without_auth(self):
        """
        User cannot unfollow another user if he/she are not
        logged in
        """
        with self.settings(
                EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
            self.register_user(self.user1)
        self.client.post(self.follow_url, format='json')
        response = self.client.delete(self.unfollow_url,
                                      data=self.followed_user)
        self.assertEqual(response.data['detail'],
                         "Authentication credentials were not provided.")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_list_of_following_users_with_auth(self):
        """
        User can get a list of users that he is currently following
        """
        with self.settings(
                EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
            self.authorize_user(self.user)
            self.register_user(self.user1)
            self.client.post(self.follow_url, format='json')
            response = self.client.get(self.following_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_list_of_following_users_without_auth(self):
        """
        User should not get a list of users that he is
        currently following without authentication
        """
        self.authorize_user(self.user)
        with self.settings(
                EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
            self.register_user(self.user1)
            response = self.client.get(self.following_list_url)
        self.assertEqual(response.content,
                         b'{"following": []}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_list_of_followers_with_auth(self):
        """
        User can get a list of users that are following him
        """
        with self.settings(
                EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
            self.authorize_user(self.user)
            response = self.client.get(self.followers_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_list_of_followers_without_auth(self):
        """
        User should not get a list of users that are
        currently following him/her without authentication
        """
        with self.settings(
                EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
            response = self.client.get(self.followers_url)
        self.assertEqual(response.data['detail'],
                         "Authentication credentials were not provided.")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
