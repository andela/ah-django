from ...authentication.tests.base_test import BaseTestCase
from rest_framework_jwt import utils
from ..models import Article, Report
from ..serializers import ArticleSerializer, ReportSerializer
from ..views import NewArticle
from rest_framework import status


class TestNewArticle(BaseTestCase):
    """
        New article tests
    """

    def test_auth_required(self):
        """
            auth required to post article
        """
        new_article = {
            "article": {
                "title": "How to train your dragon",
                "description": "Ever wonder how?",
                "body": "It takes a Jacobian",
                "tagList": [
                    "dragons",
                    "training"
                ]
            }
        }

        response = self.client.post(self.new_article_path,
                                    new_article, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_new(self):
        """
        create new article successfuly
        """
        new_article = {
            "article": {
                "title": "How to train your dragon",
                "description": "Ever wonder how?",
                "body": "It takes a Jacobian",
                "tagList": [
                    "dragons",
                    "training"
                ]
            }
        }

        payload = utils.jwt_payload_handler(self.testuser)
        token = utils.jwt_encode_handler(payload)
        auth = 'Bearer {0}'.format(token)
        response = self.client.post(self.new_article_path,
                                    new_article, HTTP_AUTHORIZATION=auth,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ArticleDetails(BaseTestCase):
    """
        Test getting, updating, deleting articles
    """

    def test_get_all_articles(self):
        """
        test get all articles
        """
        response = self.client.get(self.articles_feed)
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        print("response.data==>", response.data['results'])
        print("serializer.data", serializer.data)
        self.assertEqual(response.data['results'], serializer.data[0:5])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_article(self):
        """
        test get one article
        """
        response = self.client.get(self.article_details)
        articles = Article.objects.get(slug='test-slug')
        serializer = ArticleSerializer(articles)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_article(self):
        """
        test update article
        """
        update_article = {
            "title": "How to train your dragon -- update",
            "description": "Ever wonder how?",
            "body": "It takes a Jacobian",
            "tagList": [
                "dragons",
                "training"
            ]
        }

        payload = utils.jwt_payload_handler(self.testuser)
        token = utils.jwt_encode_handler(payload)
        auth = 'Bearer {0}'.format(token)
        response = self.client.put(self.article_details,
                                   update_article,
                                   HTTP_AUTHORIZATION=auth,
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_article(self):
        """
        test update article unauthorized
        """
        update_article = {
            "title": "How to train your dragon -- update",
            "description": "Ever wonder how?",
            "body": "It takes a Jacobian",
            "tagList": [
                "dragons",
                "training"
            ]
        }
        response = self.client.put(self.article_details,
                                   update_article, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_article(self):
        """
        test delete article
        """
        payload = utils.jwt_payload_handler(self.testuser)
        token = utils.jwt_encode_handler(payload)
        auth = 'Bearer {0}'.format(token)
        response = self.client.put(self.article_details,
                                   HTTP_AUTHORIZATION=auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_delete_article(self):
        """
        test delete article unauthorized
        """
        response = self.client.put(self.article_details)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_rate_article(self):
        """
        test rate article
        """
        rating = {
            "rating": {
                "rating": 4
            }
        }

        payload = utils.jwt_payload_handler(self.testuser)
        token = utils.jwt_encode_handler(payload)
        auth = 'Bearer {0}'.format(token)
        response = self.client.post(self.article_rating,
                                    rating, HTTP_AUTHORIZATION=auth,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_rate_article(self):
        """
        test rate article invalid
        """
        rating = {
            "rating": {
                "rating": 23
            }
        }

        payload = utils.jwt_payload_handler(self.testuser)
        token = utils.jwt_encode_handler(payload)
        auth = 'Bearer {0}'.format(token)
        response = self.client.post(self.article_rating,
                                    rating, HTTP_AUTHORIZATION=auth,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_calculate_reading_time(self):
        """
        test time calculation
        """
        short_post = NewArticle.calculate_read_time("very short post")
        self.assertEqual(short_post, "less than 1 minute")
        longer_post_body = 'The incident that ruined my day happened early ' \
                           'in the morning: I was in my car and ' \
                           'inadvertently cut off another driver, who then ' \
                           'zoomed up next to me and yelled, “Idiot!” ' \
                           'outside my window before hastily driving off. ' \
                           'Frustrated, I yelled something nasty back, ' \
                           'even though I knew he couldn’t hear me — which ' \
                           'frustrated me, too.Even minor annoyances like ' \
                           'these can create a domino effect. The first ' \
                           'annoyance magnifies each one that follows, ' \
                           'all of them building on each other until you’ve ' \
                           'worked yourself into a full-on bad mood.But ' \
                           'there are ways you can successfully lessen your ' \
                           'negative reactions before they escalate. When ' \
                           'you feel the day spiraling away from you, ' \
                           'simply noticing that you’re in a funk is an ' \
                           'important first step toward getting out of it. ' \
                           'Here are a few ways to pull yourself out of a ' \
                           'bad mood before it gets too big to ' \
                           'control.Triggers can be physical, too. For ' \
                           'instance, I have a bad habit of drinking too ' \
                           'much coffee and little else, turning me into a ' \
                           'jittery, dehydrated mess. According to Hanley, ' \
                           'a small detail like this can be a contributing ' \
                           'factor to a bad mood—and one that might be ' \
                           'easily overlooked.the correct way.” When I ' \
                           'yelled back at that other driver, ' \
                           'I was reflexively reacting. But angrily ' \
                           'lingering on the interactn for the rest of the ' \
                           'day was a choice — and one that only aggravated ' \
                           'my mood.ep back from your immediate emotional ' \
                           'reactions and reflect on them, says Leslie ' \
                           'Becker-Phelps, a licensed psychologist and ' \
                           'author of Insecure in Love. By thinking ' \
                           'critically about the situation and your role in ' \
                           'it, you can create some distance from your ' \
                           'emotions, which in turn allows you to gain more ' \
                           'control over how youre feeling. small one — you ' \
                           'forget your password for the umpteenth time, ' \
                           'or a meeting gets rescheduled yet again — it’s ' \
                           'easy to let yourself fall into a steady stream ' \
                           'of complaints. to look for threats,” Hanley ' \
                           'says. Evolutionarily, this helped keep us ' \
                           'alive — but in modn-day life, threats can look ' \
                           'a lot more like minor annoyances, creating a ' \
                           'negativity bias that keeps us focused on what’s ' \
                           'going wrong. “To bust out of this neural rut,' \
                           '” she says, “train yourself to acknowledge when ' \
                           'things go right.n each of those things. “It’s a ' \
                           'way for you to say, ‘I had a positive impact,' \
                           '’” Colan says. “And I don’t care how much of a ' \
                           'bummer your day is, there’s always a couple of ' \
                           'things that went well.” Themore attuned you are ' \
                           'to this fact, the better equipped you’ll be to ' \
                           'consciously respond with positivity the next ' \
                           'time things go wrong. let something derail your ' \
                           'mood and your day. That’s a skill that comes ' \
                           'with time and practice.” Hanley says. “Even ' \
                           'saying to yourself, ‘Wow, I’m in a bad mood,' \
                           '’ can be just the opening to ask yourself, ' \
                           '‘What do I most ned right now?’”it in the first ' \
                           'place. Make an efort to regularly check in with ' \
                           'yourself througout the day for what you need in ' \
                           'a given moment — whether it’s a glass of water ' \
                           'or a quick walk around the block. Colan says ' \
                           'there’s a level of mindfulness to it: “One of ' \
                           'the key things to get through any point of ' \
                           'adversity—even if it’s just a bad mood or rough ' \
                           'day—you have to plan for the future but live in ' \
                           'the present.mporary may help speed the process ' \
                           'along. '
        longer_post = NewArticle.calculate_read_time(longer_post_body)
        self.assertNotEqual(longer_post, "less than 1 minute")

    def test_pagination(self):
        response = self.client.get('/api/articles/feed/?page=1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_existent_page(self):
        response = self.client.get('/api/articles/feed/?page=10000')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def search_article_title_success(self):
        """ test for a successful search for article by title"""
        response = self.test_client.get(
            "/api/articles/search?title={}".format(self.title),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_report_article(self):
        """
        test report a single article
        """
        message = {
            "message": "I hate this article"
        }
        payload = utils.jwt_payload_handler(self.testuser)
        token = utils.jwt_encode_handler(payload)
        auth = 'Bearer {0}'.format(token)
        res = self.client.post(self.report_article,
                               message,
                               HTTP_AUTHORIZATION=auth,
                               format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_report_article_invalid_message(self):
        """
        test report a single article using invalid message
        """
        message = {
            "message": ""
        }
        payload = utils.jwt_payload_handler(self.testuser)
        token = utils.jwt_encode_handler(payload)
        auth = 'Bearer {0}'.format(token)
        res = self.client.post(self.report_article,
                               message,
                               HTTP_AUTHORIZATION=auth,
                               format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_admin_get_all_reported_articles(self):
        """
        test admin see all reported articles
        """
        self.login_superuser()
        response = self.client.get(self.view_reports)
        reports = Report.objects.all()
        serializer = ReportSerializer(reports, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
