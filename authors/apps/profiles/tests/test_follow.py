"""
this file contains all tests pertaining following a user
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

    def test_get_user_followers(self):
        onsignup = self.signup()
        user = json.loads(onsignup.content)["user"]
        res = self.client.get(
            "/api/users/{}/followers/".format(user["username"]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(res.content),
                         {
            "followers": []
        })

    def test_get_user_followers_after_following(self):
        onsignup = self.signup()
        user = json.loads(onsignup.content)["user"]
        newuser = self.signupnewuser()
        # user2 follows user1
        # get token
        newusertoken = json.loads(newuser.content)["user"]["token"]
        # follow
        self.client.post(
            "/api/users/{}/follow/".format(
                user["username"]),
            HTTP_AUTHORIZATION='bearer {}'.format(newusertoken),
            format="json")
        # get followers
        res = self.client.get(
            "/api/users/{}/followers/".format(user["username"]))
        self.assertEqual(json.loads(res.content),
                         {
            "followers": [{
                "username": "PremierMember2",
                "firstname": "",
                "lastname": "",
                "bio": "",
                "fullname": " ",
                "image": ""
            }]
        })

    def test_attempt_to_follow_twice(self):
        onsignup = self.signup()
        user = json.loads(onsignup.content)["user"]
        newuser = self.signupnewuser()
        # user2 follows user1
        # get token
        newusertoken = json.loads(newuser.content)["user"]["token"]
        # follow
        self.client.post(
            "/api/users/{}/follow/".format(
                user["username"]),
            HTTP_AUTHORIZATION='bearer {}'.format(newusertoken),
            format="json")
        # try following again
        follow_twice = self.client.post(
            "/api/users/{}/follow/".format(
                user["username"]),
            HTTP_AUTHORIZATION='bearer {}'.format(newusertoken),
            format="json")
        self.assertEqual(follow_twice.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(json.loads(follow_twice.content),
                         {
            "error": "You follow PremierMember already"
        })

    def test_follow_non_existent_user(self):
        newuser = self.signupnewuser()
        newusertoken = json.loads(newuser.content)["user"]["token"]
        res = self.client.post(
            "/api/users/idontexist/follow/",
            HTTP_AUTHORIZATION='bearer {}'.format(newusertoken),
            format="json")
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json.loads(res.content),
                         {
            "error": "A User with the username idontexist is not found"
        })

    def test_following_endpoint(self):
        onsignup = self.signup()
        user = json.loads(onsignup.content)["user"]
        newuser = self.signupnewuser()
        # user2 follows user1
        # get token
        newusertoken = json.loads(newuser.content)["user"]["token"]
        # follow
        self.client.post(
            "/api/users/{}/follow/".format(
                user["username"]),
            HTTP_AUTHORIZATION='bearer {}'.format(newusertoken),
            format="json")
        newuserusername = json.loads(newuser.content)["user"]["username"]
        res = self.client.get(
            "/api/users/{}/following/".format(newuserusername))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(res.content), {
            "following": [{
                "bio": "",
                "firstname": "",
                "fullname": " ",
                "lastname": "",
                "image": "",
                "username": "PremierMember"
            }]
        })

    def test_get_non_existent_users_following_list(self):
        res = self.client.get(
            "/api/users/idontexist/following/")
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json.loads(res.content), {
            "error": "A User with the username idontexist is not found"
        })
