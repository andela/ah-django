from django.core import mail
from rest_framework.test import APITestCase, APIClient
import json


class EmailTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.followuser_url = "/api/users/{}/follow/"
        self.createarticle_url = "/api/articles/"
        self.subscription_url = '/api/subscription/{}/'

        self.article = {
            "article": {
                "title": "This is the article title",
                "description": "This is the article description",
                "body": "This is the article body",
                "image_url": "https://imageurl.com",
                "tags": ["test", "trial"]
            }

        }

    def signupuser1(self):
        user_1 = {
            "user": {
                "email": "premiermember@gmail.com",
                "username": "premiermember",
                "password": "premiermember2019"
            }
        }
        res = self.client.post(
            "/api/users", user_1, format="json")
        self.token1 = json.loads(res.content)["user"]["token"]

    def signupuser2(self):
        user_1 = {
            "user": {
                "email": "profilemania@gmail.com",
                "password": "profiles2019",
                "username": "profmania"
            }
        }
        res = self.client.post(
            "/api/users", user_1, format="json")
        self.token2 = json.loads(res.content)["user"]["token"]

    def signupuser3(self):
        user_3 = {
            "user": {
                "email": "third@gmail.com",
                "password": "third2019",
                "username": "third"
            }
        }
        res = self.client.post(
            "/api/users", user_3, format="json")
        self.token3 = json.loads(res.content)["user"]["token"]

    def user2followuser1(self):
        self.signupuser1()
        self.signupuser2()
        self.client.post(
            self.followuser_url.format(
                "premiermember"),
            HTTP_AUTHORIZATION='bearer {}'.format(self.token2),
            format="json")

    def user2creating_a_comment(self):
        comment = {
            "comment": {
                "body": "New comment"
            }
        }
        self.client.post("/api/articles/this-is-the-article-title/comments",
                         comment,
                         HTTP_AUTHORIZATION='bearer {}'.format(self.token2),
                         format="json"
                         )

    def user_3_favoriting_the_article(self):
        self.client.post("/api/articles/this-is-the-article-title/favorite",
                         HTTP_AUTHORIZATION='bearer {}'.format(self.token3)
                         )

    def user1create_article(self):
        self.client.post(
            self.createarticle_url,
            self.article,
            HTTP_AUTHORIZATION='bearer {}'.format(self.token1),
            format="json")

    def user_two_opting_out_of_email(self):
        self.client.delete(
            self.subscription_url.format("email"),
            {},
            format="json",
            HTTP_AUTHORIZATION='bearer {}'.format(self.token2))

    def test_receive_notification_on_following_user(self):
        self.user2followuser1()
        self.assertEqual(len(mail.outbox), 3)
        # 2 emails are for account creation and the last one is for
        # user2 following user1
        self.assertEqual(
            [m.subject for m in mail.outbox],
            ['Welcome to Authors Haven',
             'Welcome to Authors Haven',
             'You have a new follower'])

    def test_send_email_on_new_article_creation(self):
        self.user2followuser1()
        self.user1create_article()
        # the mail outbox is 4 because of the 2 registrations
        # the 3rd is for following a user
        # and the new
        # email that is to be sent pertaining the new article.
        self.assertEqual(len(mail.outbox), 4)
        self.assertEqual(mail.outbox[3].subject, "premiermember's New Article")

    def test_if_notification_will_be_sent_via_email_on_unsubscribing(self):
        self.user2followuser1()
        self.user_two_opting_out_of_email()
        self.user1create_article()
        # if you opt out no email will be sent to you.
        # the two emails in the outbox are for account registration.
        # the third email is for following a user.
        self.assertEqual(len(mail.outbox), 3)

    def test_if_notification_is_received_after_favoriting(self):
        self.user2followuser1()
        # we want user 2 to opt out of emails
        self.user_two_opting_out_of_email()
        self.user1create_article()
        self.signupuser3()
        self.user_3_favoriting_the_article()
        self.user2creating_a_comment()
        # the emails will be 5
        # 3 for registering the 3 users
        # the fourth will be for user2 following user1
        # the fifth one is for the comment.
        self.assertEqual(len(mail.outbox), 5)
        self.assertEqual(mail.outbox[4].subject,
                         "A New comment has been posted by profmania")
