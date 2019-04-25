"""
this file contains all tests pertaining bookmarking of notifications.
"""
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
import json


class OptInTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_1 = {
            "user": {
                "email": "premiermember@gmail.com",
                "username": "premiermember",
                "password": "premiermember2019"
            }
        }
        self.subscription_url = '/api/subscription/{}/'

    def signup(self):
        res = self.client.post(
            "/api/users", self.user_1, format="json")
        return json.loads(res.content)["user"]["token"]

    def test_opt_in_to_email_incognito(self):
        post = self.client.post(
            self.subscription_url.format("email"),
            {},
            format="json")
        self.assertEqual(post.status_code,
                         status.HTTP_403_FORBIDDEN)

    def test_opt_in_to_unknown_type(self):
        post = self.client.post(
            self.subscription_url.format("notvalid"),
            {},
            format="json",
            HTTP_AUTHORIZATION='bearer {}'.format(self.signup()))
        self.assertEqual(post.status_code,
                         status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(post.content)["error"],
            "The type should either be (email) or (in_app)")

    def test_opt_in_already_opted_in_email(self):
        post = self.client.post(
            self.subscription_url.format("email"),
            {},
            format="json",
            HTTP_AUTHORIZATION='bearer {}'.format(self.signup()))
        self.assertEqual(post.status_code,
                         status.HTTP_409_CONFLICT)
        self.assertEqual(
            json.loads(post.content)["error"],
            "You are already opted into email notifications")

    def test_opt_in_already_opted_in_in_app(self):
        post = self.client.post(
            self.subscription_url.format("in_app"),
            {},
            format="json",
            HTTP_AUTHORIZATION='bearer {}'.format(self.signup()))
        self.assertEqual(post.status_code,
                         status.HTTP_409_CONFLICT)
        self.assertEqual(
            json.loads(post.content)["error"],
            "You are already opted into in_app notifications")

    # test unsubscribing
    def test_opt_out_of_email(self):
        post = self.client.delete(
            self.subscription_url.format("email"),
            {},
            format="json",
            HTTP_AUTHORIZATION='bearer {}'.format(self.signup()))
        self.assertEqual(post.status_code,
                         status.HTTP_200_OK)

    def test_opt_out_of_in_app_notifications(self):
        post = self.client.delete(
            self.subscription_url.format("in_app"),
            {},
            format="json",
            HTTP_AUTHORIZATION='bearer {}'.format(self.signup()))
        self.assertEqual(post.status_code,
                         status.HTTP_200_OK)

    def test_opt_out_of_not_valid_type(self):
        post = self.client.delete(
            self.subscription_url.format("notexist"),
            {},
            format="json",
            HTTP_AUTHORIZATION='bearer {}'.format(self.signup()))
        self.assertEqual(post.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_opt_out_incognito(self):
        post = self.client.delete(
            self.subscription_url.format("notexist"),
            {},
            format="json")
        self.assertEqual(post.status_code,
                         status.HTTP_403_FORBIDDEN)

    def test_opt_out_and_back_in_of_both(self):
        token = self.signup()
        self.client.delete(
            self.subscription_url.format("email"),
            {},
            format="json",
            HTTP_AUTHORIZATION='bearer {}'.format(token))
        self.client.delete(
            self.subscription_url.format("in_app"),
            {},
            format="json",
            HTTP_AUTHORIZATION='bearer {}'.format(token))

        postemail = self.client.post(
            self.subscription_url.format("email"),
            {},
            format="json",
            HTTP_AUTHORIZATION='bearer {}'.format(token))
        self.assertEqual(postemail.status_code,
                         status.HTTP_200_OK)
        postin_app = self.client.post(
            self.subscription_url.format("in_app"),
            {},
            format="json",
            HTTP_AUTHORIZATION='bearer {}'.format(token))
        self.assertEqual(postin_app.status_code,
                         status.HTTP_200_OK)

    def test_attempt_to_opt_out_twice(self):
        token = self.signup()
        self.client.delete(
            self.subscription_url.format("in_app"),
            {},
            format="json",
            HTTP_AUTHORIZATION='bearer {}'.format(token))
        self.client.delete(
            self.subscription_url.format("email"),
            {},
            format="json",
            HTTP_AUTHORIZATION='bearer {}'.format(token))
        in_app = self.client.delete(
            self.subscription_url.format("in_app"),
            {},
            format="json",
            HTTP_AUTHORIZATION='bearer {}'.format(token))
        email = self.client.delete(
            self.subscription_url.format("email"),
            {},
            format="json",
            HTTP_AUTHORIZATION='bearer {}'.format(token))

        self.assertEqual(in_app.status_code,
                         status.HTTP_409_CONFLICT)
        self.assertEqual(email.status_code,
                         status.HTTP_409_CONFLICT)
        self.assertEqual(
            json.loads(email.content)["error"],
            "You are already opted out of email notifications")
