from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
import json


class CURDArticlesTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.postlist_article_url = '/api/articles/'
        self.filter_article_url = '/api/articles?title=article&author_id=1'
        self.get_article_url = '/api/articles/{article_slug}/'
        self.get_tag_url = '/api/tags'
        self.user_signup = {
            "user": {
                "email": "testuser@gmail.com",
                "username": "testuser",
                "password": "testuserpass123"
            }
        }

        self.user_signup2 = {
            "user": {
                "email": "testuser2@gmail.com",
                "username": "testuser2",
                "password": "testuser2pass123"
            }
        }

        self.article = {
            "article": {
                "title": "This is the article title",
                "description": "This is the article description",
                "body": "This is the article body",
                "image_url": "https://imageurl.com",
                "tags": ["test", "trial"]
            }

        }

        self.article_no_tags = {
            "article": {
                "title": "This is the article title",
                "description": "This is the article description",
                "body": "This is the article body",
                "image_url": "https://imageurl.com"
            }

        }

        self.article_empty_taglist = {
            "article": {
                "title": "This is the article title",
                "description": "This is the article description",
                "body": "This is the article body",
                "image_url": "https://imageurl.com",
                "tags": []
            }

        }

        self.edit_article = {
            "title": "This article title is edited",
            "body": "This article body is edited",
            "tags": ["test", "trial"]

        }

        self.signup = self.client.post(
            "/api/users",
            self.user_signup,
            format="json"
        )

        self.signup2 = self.client.post(
            "/api/users",
            self.user_signup2,
            format="json"
        )

        self.credentials = json.loads(self.signup.content)[
            "user"]["token"]
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.credentials)

    def create_article(self, data=None):
        """ method for creating and article """
        data = data

        return self.client.post(
            self.postlist_article_url,
            data,
            format='json', follow=True
        )

    def test_create_article(self):
        article = self.create_article(self.article)

        self.assertEqual(article.status_code,
                         status.HTTP_201_CREATED)

    def test_create_article_no_tags(self):
        article = self.create_article(self.article_no_tags)

        self.assertEqual(article.status_code,
                         status.HTTP_201_CREATED)

    def test_create_article_empty_taglist(self):
        article = self.create_article(self.article_empty_taglist)

        self.assertEqual(article.status_code,
                         status.HTTP_201_CREATED)

    def test_get_taglist(self):
        self.create_article(self.article)
        get_tag = self.client.get(
            self.get_tag_url
        )
        self.assertEqual(get_tag.status_code,
                         status.HTTP_200_OK)

    def test_list_articles(self):
        self.create_article(self.article)
        list_articles = self.client.get(
            self.postlist_article_url, follow=True
        )
        self.assertEqual(list_articles.status_code,
                         status.HTTP_200_OK)

    def test_get_article(self):
        article = self.create_article(self.article)
        data = json.loads(article.content)
        article_slug = data['article']['slug']
        get_articles = self.client.get(
            self.get_article_url.format(article_slug=article_slug)
        )

        self.assertEqual(get_articles.status_code,
                         status.HTTP_200_OK)

    def test_put_article(self):
        article = self.create_article(
            self.article)
        data = json.loads(article.content)
        article_slug = data['article']['slug']
        edit_article = self.client.put(
            self.get_article_url.format(article_slug=article_slug),
            data=self.edit_article, formart='json'
        )

        self.assertEqual(edit_article.status_code,
                         status.HTTP_200_OK)

    def test_delete_article(self):
        article = self.create_article(
            self.article)
        data = json.loads(article.content)
        article_slug = data['article']['slug']
        delete_article = self.client.delete(
            self.get_article_url.format(article_slug=article_slug)
        )
        self.assertEqual(delete_article.status_code,
                         status.HTTP_204_NO_CONTENT)

    def test_invalid_user(self):
        """
        Test post without login
        """
        self.client.credentials()
        article = self.create_article(self.article)
        self.assertEqual(article.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthrosed_user_delete(self):
        """
        Test unauthorised user
        deleting an article
        """
        article = self.create_article(
            self.article)
        self.client.credentials()
        credentials2 = json.loads(self.signup2.content)[
            "user"]["token"]
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + credentials2)
        data = json.loads(article.content)
        article_slug = data['article']['slug']
        delete_article = self.client.delete(
            self.get_article_url.format(article_slug=article_slug)
        )
        self.assertEqual(delete_article.status_code,
                         status.HTTP_401_UNAUTHORIZED)

    def test_unauthrosed_user_patch(self):
        """
        Test unauthorised user
        deleting an article
        """
        article = self.create_article(
            self.article)
        self.client.credentials()
        credentials2 = json.loads(self.signup2.content)[
            "user"]["token"]
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + credentials2)
        data = json.loads(article.content)
        article_slug = data['article']['slug']
        edit_article = self.client.put(
            self.get_article_url.format(article_slug=article_slug),
            data=self.edit_article, formart='json'
        )

        self.assertEqual(edit_article.status_code,
                         status.HTTP_401_UNAUTHORIZED)
        get_articles = self.client.get(
            self.get_article_url.format(article_slug=article_slug)
        )

        self.assertEqual(get_articles.status_code,
                         status.HTTP_200_OK)
# Rating Tests

    def test_create_rating(self):
        article = self.create_article(self.article)
        data = json.loads(article.content)
        article_id = data['article']['id']
        self.rate_article_url = "/api/articles/{article_id}/rating/"
        payload = {"rating":
                   {
                       "rating": 2
                   }
                   }
        rate_article = self.client.post(
            self.rate_article_url.format(article_id=article_id),
            data=payload, format='json'
        )
        self.assertEqual(rate_article.status_code,
                         status.HTTP_200_OK)

    def test_create_rating_article_missing(self):
        self.rate_article_url = "/api/articles/{article_id}/rating/"
        payload = {"rating":
                   {
                       "rating": 2
                   }
                   }
        rate_article = self.client.post(
            self.rate_article_url.format(article_id=123),
            data=payload, format='json'
        )
        self.assertEqual(rate_article.status_code,
                         status.HTTP_404_NOT_FOUND)

    def test_create_rating_field_missing(self):
        article = self.create_article(self.article)
        data = json.loads(article.content)
        article_id = data['article']['id']
        self.rate_article_url = "/api/articles/{article_id}/rating/"
        payload = {"rating":
                   {
                   }
                   }
        rate_article = self.client.post(
            self.rate_article_url.format(article_id=article_id),
            data=payload, format='json'
        )
        self.assertEqual(rate_article.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_create_rating_non_integer_rating(self):
        article = self.create_article(self.article)
        data = json.loads(article.content)
        article_id = data['article']['id']
        self.rate_article_url = "/api/articles/{article_id}/rating/"
        payload = {"rating":
                   {
                       "rating": "five"
                   }
                   }
        rate_article = self.client.post(
            self.rate_article_url.format(article_id=article_id),
            data=payload, format='json'
        )
        self.assertEqual(rate_article.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_pagination_by_page_size(self):
        """Test pagination when passing page size as query param """

        self.list_article_url = '/api/articles/?page_size=4'
        for i in range(10):
            self.create_article(self.article)

        response = self.client.get(self.list_article_url)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)
        self.assertEqual(len(data["articles"]), 4)

    def test_default_pagination(self):
        """Test default pagination of articles """

        self.list_article_url = '/api/articles'
        for i in range(20):
            self.create_article(self.article)

        response = self.client.get(self.list_article_url)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)
        self.assertEqual(len(data["articles"]), 12)

    def test_filtered_article(self):
        """Test filtering articles"""

        self.create_article(self.article)
        list_articles = self.client.get(
            self.filter_article_url, follow=True
        )
        self.assertEqual(list_articles.status_code,
                         status.HTTP_200_OK)

    def test_get_article_read_time(self):
        """ Test time it takes to read an article"""

        article = self.create_article(self.article)
        data = json.loads(article.content)
        article_slug = data['article']['slug']
        response = self.client.get(
            self.get_article_url.format(article_slug=article_slug)
        )
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)
        self.assertEqual(data['article']['read_time'], '1 min read')

# Social sharing tests
    def test_share_via_email(self):
        article = self.create_article(self.article)
        data = json.loads(article.content)
        article_slug = data['article']['slug']
        self.share_article_url = "/api/articles/{article_slug}/share/email/"
        payload = {"email": "tonywamuriithi@gmail.com"
                   }
        share_article = self.client.post(
            self.share_article_url.format(article_slug=article_slug),
            data=payload, format='json'
        )
        self.assertEqual(share_article.status_code, status.HTTP_200_OK)
        self.assertIn("shared_link", share_article.data)

    def test_share_via_facebook(self):
        article = self.create_article(self.article)
        data = json.loads(article.content)
        article_slug = data['article']['slug']
        self.share_article_url = "/api/articles/{article_slug}/share/facebook/"
        share_article = self.client.post(
            self.share_article_url.format(article_slug=article_slug),
            format='json'
        )
        self.assertEqual(share_article.status_code, status.HTTP_200_OK)
        self.assertIn("shared_link", share_article.data)

    def test_share_via_twitter(self):
        article = self.create_article(self.article)
        data = json.loads(article.content)
        article_slug = data['article']['slug']
        self.share_article_url = "/api/articles/{article_slug}/share/twitter/"
        share_article = self.client.post(
            self.share_article_url.format(article_slug=article_slug),
            format='json'
        )
        self.assertEqual(share_article.status_code, status.HTTP_200_OK)
        self.assertIn("shared_link", share_article.data)

    def test_share_via_email_non_existent_article(self):
        article = self.create_article(self.article)
        data = json.loads(article.content)
        article_slug = data['article']['slug']
        self.share_article_url = "/api/articles/{article_slug}567/share/email/"
        payload = {"email": "tonywamuriithi@gmail.com"
                   }
        share_article = self.client.post(
            self.share_article_url.format(article_slug=article_slug),
            data=payload, format='json'
        )
        self.assertEqual(share_article.status_code, status.HTTP_404_NOT_FOUND)

    def test_share_via_facebook_non_existent_article(self):
        article = self.create_article(self.article)
        data = json.loads(article.content)
        article_slug = data['article']['slug']
        self.share_artcle_url = "/api/articles/{article_slug}5/share/facebook/"
        share_article = self.client.post(
            self.share_artcle_url.format(article_slug=article_slug),
            format='json'
        )
        self.assertEqual(share_article.status_code, status.HTTP_404_NOT_FOUND)

    def test_share_via_twitter_non_existent_article(self):
        article = self.create_article(self.article)
        data = json.loads(article.content)
        article_slug = data['article']['slug']
        self.share_article_url = "/api/articles/{article_slug}5/share/twitter/"
        share_article = self.client.post(
            self.share_article_url.format(article_slug=article_slug),
            format='json'
        )
        self.assertEqual(share_article.status_code, status.HTTP_404_NOT_FOUND)

    def test_share_via_email_without_receivers_email(self):
        article = self.create_article(self.article)
        data = json.loads(article.content)
        article_slug = data['article']['slug']
        self.share_article_url = "/api/articles/{article_slug}/share/email/"
        payload = {"email": ""
                   }
        share_article = self.client.post(
            self.share_article_url.format(article_slug=article_slug),
            data=payload, format='json'
        )

        self.assertEqual(share_article.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_share_via_email_with_invalid_receivers_email(self):
        article = self.create_article(self.article)
        data = json.loads(article.content)
        article_slug = data['article']['slug']
        self.share_article_url = "/api/articles/{article_slug}/share/email/"
        payload = {"email": "tonywamuriithigmail.com"
                   }
        share_article = self.client.post(
            self.share_article_url.format(article_slug=article_slug),
            data=payload, format='json'
        )

        self.assertEqual(share_article.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_share_via_email_by_others(self):
        article = self.create_article(
            self.article)
        self.client.credentials()
        credentials2 = json.loads(self.signup2.content)[
            "user"]["token"]
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + credentials2)
        data = json.loads(article.content)
        article_slug = data['article']['slug']
        self.share_article_url = "/api/articles/{article_slug}/share/email/"
        payload = {"email": "tonywamuriithi@gmail.com"
                   }
        share_article = self.client.post(
            self.share_article_url.format(article_slug=article_slug),
            data=payload, format='json'
        )
        self.assertEqual(share_article.status_code, status.HTTP_200_OK)
        self.assertIn("shared_link", share_article.data)

    def test_share_via_facebook_by_others(self):
        article = self.create_article(
            self.article)
        self.client.credentials()
        credentials2 = json.loads(self.signup2.content)[
            "user"]["token"]
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + credentials2)
        data = json.loads(article.content)
        article_slug = data['article']['slug']
        self.share_article_url = "/api/articles/{article_slug}/share/facebook/"
        share_article = self.client.post(
            self.share_article_url.format(article_slug=article_slug),
            format='json'
        )
        self.assertEqual(share_article.status_code, status.HTTP_200_OK)
        self.assertIn("shared_link", share_article.data)

    def test_share_via_twitter_by_others(self):
        article = self.create_article(
            self.article)
        self.client.credentials()
        credentials2 = json.loads(self.signup2.content)[
            "user"]["token"]
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + credentials2)
        data = json.loads(article.content)
        article_slug = data['article']['slug']
        self.share_article_url = "/api/articles/{article_slug}/share/twitter/"
        share_article = self.client.post(
            self.share_article_url.format(article_slug=article_slug),
            format='json'
        )

        self.assertEqual(share_article.status_code, status.HTTP_200_OK)
        self.assertIn("shared_link", share_article.data)
