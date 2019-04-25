from rest_framework.views import status
import json
from authors.apps.authentication.tests.basetest import BaseTestCase


class ProfileUpdateClass(BaseTestCase):
    def test_update_bio_firstname_and_lastname(self):
        # its worth noting that you can update
        # just the fields that you require.
        # that can be one field or all the fields.
        newbio = {
            "bio": "New Bio",
            "firstname": "First",
            "lastname": "Last"
        }
        update_profile = self.client.put(
            "/api/profiles/premiermember/",
            data=newbio,
            HTTP_AUTHORIZATION='bearer {}'.format(self.token),
            format="json")
        self.assertEqual(update_profile.status_code,
                         status.HTTP_200_OK)
        self.assertEqual(json.loads(update_profile.content)
                         ["profile"]["bio"], "New Bio")
        self.assertEqual(json.loads(update_profile.content)
                         ["profile"]["firstname"], "First")
        self.assertEqual(json.loads(update_profile.content)
                         ["profile"]["lastname"], "Last")
        self.assertEqual(json.loads(update_profile.content)
                         ["profile"]["fullname"], "First Last")

    def test_update_bio_with_no_credentials(self):
        newbio = {
            "bio": "New Anonymous Bio"
        }
        update_profile = self.client.put(
            "/api/profiles/premiermember/",
            data=newbio,
            format="json")
        self.assertEqual(update_profile.status_code,
                         status.HTTP_403_FORBIDDEN)

    def test_unauthorized_user_update_profile(self):
        user_2 = {
            "user": {
                "email": "premiermemberanonymous@gmail.com",
                "username": "premiermember_anonymous",
                "password": "premiermember2019"
            }
        }
        newanonymousbio = {
            "bio": "New Anonymous Bio"
        }
        newseconduser = self.client.post(
            "/api/users", user_2, format="json")
        token = json.loads(newseconduser.content)[
            "user"]["token"]

        update_profile = self.client.put(
            "/api/profiles/premiermember/",
            data=newanonymousbio,
            HTTP_AUTHORIZATION='bearer {}'.format(token),
            format="json")
        self.assertEqual(update_profile.status_code,
                         status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(update_profile.content)
                         ["error"],
                         "You are not allowed to edit or delete this profile")

    def test_update_bio_with_poorly_formated_image_field(self):
        newbio = {
            "image": "new image"
        }
        update_profile = self.client.put(
            "/api/profiles/premiermember/",
            data=newbio,
            HTTP_AUTHORIZATION='bearer {}'.format(self.token),
            format="json")
        self.assertEqual(update_profile.status_code,
                         status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(update_profile.content)
                         ["errors"]["image"], ["Enter a valid URL."])
