"""
this file contains all tests pertaining unfollowing
"""
# import json
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
import json

# import pdb


class RegistrationTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_1 = {
            "user": {
                "email": "premiermember@gmail.com",
                "username": "PremierMember",
                "password": "premiermember2019"
            }
        }

    def signup(self):
        return self.client.post(
            "/api/users", self.user_1, format="json")

    def signupnewuser(self):
        user_to_follow = {
            "user": {
                "email": "premiermember2@gmail.com",
                "username": "PremierMember2",
                "password": "premiermember2019"
            }
        }
        return self.client.post(
            "/api/users", user_to_follow, format="json")

    def follow_user1(self):
        onsignup = self.signup()
        self.user = json.loads(onsignup.content)["user"]
        newuser = self.signupnewuser()
        # user2 follows user1
        # get token
        self.newusertoken = json.loads(newuser.content)["user"]["token"]
        # follow
        self.client.post(
            "/api/users/{}/follow/".format(
                self.user["username"]),
            HTTP_AUTHORIZATION='bearer {}'.format(self.newusertoken),
            format="json")

    def test_unfollow_user_who_i_had_followed(self):
        self.follow_user1()
        res = self.client.delete(
            "/api/users/{}/unfollow/".format(self.user["username"]),
            HTTP_AUTHORIZATION='bearer {}'.format(self.newusertoken))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(res.content), {
            "data": "You have successfully unfollowed PremierMember"
        })
        newres = self.client.get(
            "/api/users/{}/followers/".format(self.user["username"]))
        self.assertEqual(json.loads(newres.content), {
            "followers": []
        })

    def test_unfollow_user_i_did_not_follow(self):
        onsignup = self.signup()
        newuser = self.signupnewuser()
        user = json.loads(onsignup.content)["user"]
        newusertoken = json.loads(newuser.content)["user"]["token"]
        res = self.client.delete(
            "/api/users/{}/unfollow/".format(user["username"]),
            HTTP_AUTHORIZATION='bearer {}'.format(newusertoken))

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json.loads(res.content), {
            "error": "You had not followed PremierMember so cannot unfollow"
        })

    def test_unfollow_non_existent_user(self):
        newuser = self.signupnewuser()
        newusertoken = json.loads(newuser.content)["user"]["token"]
        res = self.client.delete(
            "/api/users/idontexist/unfollow/",
            HTTP_AUTHORIZATION='bearer {}'.format(newusertoken))

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json.loads(res.content), {
            "error": "A User with the username idontexist was not found"
        })
