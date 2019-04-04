from rest_framework import generics, status, mixins, permissions
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Article
from .serializers import ArticleSerializer
from ..core.permissions import IsOwnerOrReadOnly
from django.template.defaultfilters import slugify


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
        return Response({"detail": "article deleted"})
