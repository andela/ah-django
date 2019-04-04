"""
this file contains all tests pertaining user login
"""
# import json
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
import json


class ProfileCreationTestClass(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_1 = {
            "user": {
                "email": "premiermember@gmail.com",
                "username": "PremierMember",
                "password": "premiermember2019"
            }
        }

    def test_bio_in_registration_response(self):
        """
        test a normal user registration with bio being returned as
        response
        """
        register_new_user = self.client.post(
            "/api/users/", self.user_1, format="json")
        self.assertEqual(register_new_user.status_code,
                         status.HTTP_201_CREATED)
        self.assertIn('bio', register_new_user.data)

    def test_image_in_registration_response(self):
        """
        test a normal user registration with image being returned as
        response
        """
        register_new_user = self.client.post(
            "/api/users/", self.user_1, format="json")
        self.assertEqual(register_new_user.status_code,
                         status.HTTP_201_CREATED)
        self.assertIn('image', register_new_user.data)

    def test_viewing_a_single_profile(self):
        """
        test getting a single profile
        """
        self.client.post(
            "/api/users/", self.user_1, format="json")
        get_profile = self.client.get("/api/profiles/premiermember/")
        self.assertEqual(get_profile.status_code,
                         status.HTTP_200_OK)

    def test_viewing_a_profile_that_doesnt_exist(self):
        """
            testing to see response a profile that doesn't exist
        """
        get_none_existent = self.client.get("/api/profiles/premiermember/")
        self.assertEqual(get_none_existent.status_code,
                         status.HTTP_404_NOT_FOUND)
        self.assertEqual(json.loads(get_none_existent.content), {
            "error": "Profile not found"
        })
