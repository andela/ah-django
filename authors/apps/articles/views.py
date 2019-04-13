from rest_framework import generics, status, mixins, exceptions
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly,
    AllowAny, IsAdminUser)
from rest_framework.response import Response
from rest_framework.views import APIView
from django_social_share.templatetags import social_share
from django.urls import reverse

from django.template.defaultfilters import slugify
from django.db.models import Avg

from .serializers import ReportSerializer
from .models import Article, ArticleRating, Report
from .exceptions import NoResultsMatch
from .serializers import ArticleSerializer, RateArticleSerializer
from ..core.permissions import IsOwnerOrReadOnly
from authors.apps.stats.models import ReadStats


def check_if_report_exists(Report, pk):

    try:
        query = Report.objects.get(pk=pk)
    except Report.DoesNotExist:
        raise exceptions.NotFound(f'Report with ID {pk} nonexistent')
    else:
        return query


class NewArticle(APIView):
    """ post:

        Creates a new article

    Provided valid article details
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = ArticleSerializer

    @staticmethod
    def calculate_read_time(article_body):
        words_per_minute = 200
        word_count = len(article_body.split(" "))
        reading_time = round(word_count / words_per_minute)
        if reading_time <= 1:
            reading_time = "less than 1 minute"
            return reading_time
        return str(reading_time) + " minutes"

    def post(self, request):
        """
            Creates a new article with the details provided
        """
        article = request.data.get('article', {})
        article['slug'] = \
            slugify(article['title']) + "_" + request.user.username
        article['reading_time'] = self.calculate_read_time(article['body'])
        serializer = self.serializer_class(data=article)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ArticleList(generics.ListAPIView):
    """ get:

            Gets all articles

        Returns a list of all posted articles
    """

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class ArticleDetails(generics.RetrieveAPIView, mixins.UpdateModelMixin,
                     generics.GenericAPIView, mixins.DestroyModelMixin):
    """ get:

            Gets a particular article

        Returns article matching slug in url
    """
    queryset = Article.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    serializer_class = ArticleSerializer
    lookup_field = 'slug'

    def get(self, request, *args, **kwargs):
        """
            Retrieves a single article item
        """
        query = self.queryset.values('author')
        owner = list(query)[0].get('author')
        self.update_author_views(author=owner)

        kwargs.update({'views': True})
        self.update_article_stats(**kwargs)

        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        data = request.data
        # check if body is being updated so we can update reading time
        if 'body' in data:
            update_reading_time = NewArticle.calculate_read_time(data['body'])
            data['reading_time'] = update_reading_time
        serializer = ArticleSerializer(request.user, data=data,
                                       partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "article deleted"},
                        status=status.HTTP_200_OK)

    @classmethod
    def update_article_stats(cls, **kwags):
        """
            Increaments the view and read-records count of
            an article
        """
        slug = kwags.get('slug')
        article = ArticleInst.fetch(slug)
        field = 'views'
        if 'views' in kwags:
            article.views += 1
        elif 'reads' in kwags:
            article.reads += 1
            field = 'reads'
            cls.update_author_views(article=article, action='reads')
        article.save(update_fields=[field])

    @classmethod
    def update_author_views(cls, article=None, author=None, action='views'):
        """
            Increaments the view count of the author
            of an article
        """
        query_field = article.author if article else author

        owner = ReadStats.objects.get(user=query_field)

        if action == 'views':
            owner.views += 1
        else:
            owner.reads += 1
        owner.save(update_fields=[action])


class ArticleInst:
    """
        Provides a helper method of retireving
        the article to commment on
    """

    @classmethod
    def fetch(cls, slug):
        """
            Retrieves an article instance by slug
        """
        try:
            article = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise exceptions.NotFound(f'Article with slug {slug} nonexistent')
        else:
            return article


class RateArticle(generics.CreateAPIView):
    """
        Allows user to post reactions to an
        article
    """
    serializer_class = RateArticleSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request, slug):
        """ post:

            Rates an article

        Rates an article with matching slug
        """
        article = ArticleInst.fetch(slug)
        rating = request.data.get('rating', {})
        serializer = self.serializer_class(data=rating)
        serializer.is_valid(raise_exception=True)

        if not isinstance(rating['rating'], int):
            return Response({"error": "rating must be an int"},
                            status=status.HTTP_400_BAD_REQUEST)

        if rating['rating'] > 5 or rating['rating'] < 1:
            return Response({"error": "rating must be 1-5"},
                            status=status.HTTP_400_BAD_REQUEST)

        ArticleRating.objects.update_or_create(
            article=article, rater=request.user, defaults=rating)
        avg = ArticleRating.objects.filter(article=article) \
            .aggregate(Avg('rating'))
        return Response({"detail": "rating posted", "avg": avg['rating__avg']},
                        status=status.HTTP_201_CREATED)


class ShareArticlesApiView(APIView):
    """
    Implements the functionality for sharing
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, **kwargs):
        """ Share to social media

        Shares to Reddit, Facebook, Twitter and Linkedin
         """
        context = {"request": request}

        platform = kwargs['platform']
        slug = kwargs['slug']

        article = Article.objects.get(slug=slug)

        if article is None:
            return Response({
                "Error": "Article not found"
            }, status.HTTP_404_NOT_FOUND)

        article_url = request.build_absolute_uri(
            reverse("articles:article_details", kwargs={"slug": article.slug})
        )

        if platform == 'facebook':
            link = social_share.post_to_facebook_url(
                context, article_url)['facebook_url']
        elif platform == 'twitter':
            link = social_share.post_to_twitter_url(
                context, "{}".format(article.title), article_url)['tweet_url']
        elif platform == 'reddit':
            link = social_share.post_to_reddit_url(
                context, article.title, article_url)['reddit_url']
        elif platform == 'linkedin':
            link = social_share.post_to_linkedin_url(
                context, article.title, article_url)['linkedin_url']

        return Response({"share": {
            "link": link,
            "resource_title": article.title,
            "provider": platform
        }}, status.HTTP_200_OK)


class SearchArticlesList(generics.ListAPIView):
    """
    This class filters articles search list
    """

    permission_classes = (AllowAny,)
    serializer_class = ArticleSerializer

    def get_queryset(self):
        # queryset = self.filter_queryset(self.get_queryset())

        queryset = Article.objects.all()
        if 'title' in self.request.query_params:
            queryset = queryset.filter(
                title__icontains=self.request.query_params['title'])
        elif 'author' in self.request.query_params:
            queryset = queryset.filter(
                author__username__icontains=self.request.
                query_params['author'])
        elif 'tag' in self.request.query_params:
            queryset = queryset.filter(
                tagList__icontains=self.request.query_params['tag'])
        else:
            queryset = []
        if len(queryset) <= 0:
            raise NoResultsMatch

        return queryset


class ReadArticleView(generics.CreateAPIView):
    """
        Sends requests to update article `read` stats
    """

    def post(self, request, slug):
        """
            Adds a READ to an article
        """
        fields = {'slug': slug,
                  'reads': True
                  }
        ArticleDetails.update_article_stats(**fields)
        res = {'message': 'Article read saved'}
        res['data'] = {'slug': slug}

        return Response(
            data=res,
            status=status.HTTP_201_CREATED)


class ReportArticleView(generics.GenericAPIView):
    """
    View for user to report article
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = ReportSerializer

    def post(self, request, slug):
        invalid_string = "Message is not a valid string"
        try:
            article = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            return Response({
                'error': f'Aricles with slug {slug} nonexistent'
            },
                status_=status.HTTP_404_NOT_FOUND)
        new_text = str(request.data.get('message', '')).strip()
        if not new_text:
            return Response({
                "details": invalid_string
            },
                status=status.HTTP_400_BAD_REQUEST)
        report = Report(
            article=article, reported_by=request.user, message=new_text)
        report.save()
        serializer = ReportSerializer(report)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReportList(generics.ListCreateAPIView):
    """
    Return all reports for admin.
    """
    permission_classes = (IsAdminUser, )
    serializer_class = ReportSerializer

    def list(self, request):
        query = Report.objects.all()
        serializer = ReportSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReportAPIViews(generics.GenericAPIView):
    """
    Functions used by admin to handle reports
    """
    permission_classes = (IsAdminUser, )
    serializer_class = ReportSerializer

    def get(self, request, pk):
        query = check_if_report_exists(Report, pk)
        serializer = ReportSerializer(query)
        query.viewed = True
        query.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    # update violation to true
    def put(self, request, pk):
        query = check_if_report_exists(Report, pk)
        serializer = ReportSerializer(query)
        query.violation = True
        query.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # delete report
    def delete(self, request, pk):
        query = check_if_report_exists(Report, pk)
        article = Article.objects.get(pk=query.article_id)
        article.delete()
        return Response({
            "details": "Report has been deleted"
        },
            status=status.HTTP_200_OK)
