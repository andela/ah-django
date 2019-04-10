from rest_framework import generics, status, mixins, exceptions
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny)
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Article, ArticleRating
from .exceptions import NoResultsMatch
from .serializers import ArticleSerializer, RateArticleSerializer
from .models import Article
from ..core.permissions import IsOwnerOrReadOnly
from django.template.defaultfilters import slugify
from django.db.models import Avg


class NewArticle(APIView):
    """ post:

        Creates a new article

    Provided valid article details
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = ArticleSerializer

    def post(self, request):
        """
            Creates a new article with the details provided
        """
        article = request.data.get('article', {})
        article['slug'] = \
            slugify(article['title']) + "_" + request.user.username
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

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "article deleted"},
                        status=status.HTTP_200_OK)


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
