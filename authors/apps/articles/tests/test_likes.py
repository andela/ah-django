from .base_test import BaseTestCase
from rest_framework.views import status
from ..models import Likes


class ArticleLikesTestCase(BaseTestCase):
    def setUp(self):
        super(ArticleLikesTestCase, self).setUp()
        self.likeUrl = "/api/articles/{}/likes/"

    def like_action(self, slug, action='like'):
        data = dict(action=action)
        return self.client.post(
            self.likeUrl.format(slug),
            data,
            format='json', follow=True)

    def test_like_article(self):
        """Tests for Article like
        """

        res = self.create_article(self.article)
        article = res.data
        article_id = article['id']
        slug = article['slug']
        like_res = self.like_action(slug)
        self.assertEqual(like_res.status_code, status.HTTP_200_OK)
        likesCount = Likes.objects.likes().filter(article_id=article_id).count()
        self.assertEqual(likesCount, 1)

    def test_like_non_existing_article(self):
        """Tests for Article like
        """
        slug = "This-is-a-none-existing-slug-for-article"
        like_res = self.like_action(slug)
        self.assertEqual(like_res.status_code, status.HTTP_404_NOT_FOUND)

    def test_dislike_article(self):
        """Tests for Article dislike
        """
        res = self.create_article(self.article)
        article = res.data
        article_id = article['id']
        slug = article['slug']
        like_res = self.like_action(slug, 'dislike')
        self.assertEqual(like_res.status_code, status.HTTP_200_OK)
        count = Likes.objects.dislikes().filter(article_id=article_id).count()
        self.assertEqual(count, 1)

    def test_delete_a_like_for_an_article(self):
        """Tests for Article Remove like
        """
        res = self.create_article(self.article)
        article = res.data
        article_id = article['id']
        slug = article['slug']
        like_res = self.like_action(slug, 'like')
        self.assertEqual(like_res.status_code, status.HTTP_200_OK)
        count = Likes.objects.likes().filter(article_id=article_id).count()
        self.assertEqual(count, 1)
        res2 = self.client.delete(self.likeUrl.format(slug))
        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        count2 = Likes.objects.likes().filter(article_id=article_id).count()
        self.assertEqual(count2, 0)

    def test_like_then_dislike_article(self):
        """Tests for Artile like then change to dislike
        """
        res = self.create_article(self.article)
        article = res.data
        article_id = article['id']
        slug = article['slug']
        like_res = self.like_action(slug, 'like')

        self.assertEqual(like_res.status_code, status.HTTP_200_OK)
        count = Likes.objects.likes().filter(article_id=article_id).count()
        self.assertEqual(count, 1)
        dislike_res = self.like_action(slug, 'dislike')
        self.assertEqual(dislike_res.status_code, status.HTTP_200_OK)
        count2 = Likes.objects.dislikes().filter(article_id=article_id).count()
        self.assertEqual(count2, 1)

    def test_get_likes_for_specific_article(self):
        """Test get likes 
        """
        res = self.create_article(self.article)
        article = res.data
        article_id = article['id']
        slug = article['slug']
        res2 = self.client.get(
            self.likeUrl.format(slug),
            format='json', follow=True)
        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        data = res2
        self.assertContains(data, 'like')
        self.assertContains(data, 'dislikes')
        self.assertContains(data, 'count')

    def test_get_likes_count_for_specific_article(self):
        """Test get likes 
        """
        res = self.create_article(self.article)
        article = res.data
        article_id = article['id']
        slug = article['slug']
        url = self.likeUrl.format(slug)
        url += 'count/'
        res2 = self.client.get(url)
        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        data = res2
        self.assertContains(data, 'like')
        self.assertContains(data, 'dislikes')
        self.assertContains(data, 'total')
