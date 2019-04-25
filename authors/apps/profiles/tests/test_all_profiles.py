"""
this file contains all tests pertaining fetching
all profiles.
"""
# import json
from authors.apps.authentication.tests.basetest import BaseTestCase
from rest_framework.views import status
import json


class RegistrationTestCase(BaseTestCase):

    def test_getting_all_profiles(self):
        """
        test getting all profiles
        """
        get_profiles = self.client.get(
            "/api/profiles/list/", format="json")
        self.assertEqual(get_profiles.status_code,
                         status.HTTP_200_OK)

    def test_searching_profiles_by_user_name(self):
        """
            test searching profiles by username
        """
        profiles = self.client.get(
            "/api/profiles/list/?search=premier",
            format="json")
        self.assertEqual(profiles.status_code, status.HTTP_200_OK)

    def test_ordering_profiles_by_username(self):
        """
            this test shows how ordering can happen with the
            username
        """
        # using a username with A so that we can see the
        # ordering in action
        first_alphabet = {
            "user": {
                "email": "acemember@gmail.com",
                "username": "ace_member",
                "password": "acemember2019"
            }
        }

        self.client.post(
            "/api/users/", first_alphabet, format="json")
        profiles = self.client.get(
            "/api/profiles/list/?ordering=user__username",
            format="json")
        self.assertEqual(profiles.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(profiles.content)[
                         0]["username"], "ace_member")
        self.assertEqual(json.loads(profiles.content)[
                         1]["username"], "premiermember")
