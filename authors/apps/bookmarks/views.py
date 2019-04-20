from rest_framework import generics, status
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly)
from rest_framework.response import (Response)
from django.db import IntegrityError

from authors.apps.articles.models import Articles
from authors.apps.articles.serializers import ArticlesSerializer
from .models import Bookmarks
from .serializers import (BookmarkSerializer, ListBookmarkersSerializer)

# Create your views here.


class ListBookmarkedArticles(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ArticlesSerializer

    def get(self, request, *args, **kwargs):
        """
            get all articles a particular user has bookmarked
        """
        articles = [n.article for n in Bookmarks.objects.filter(
            user=self.request.user)]
        return Response(data={
            "articles": self.serializer_class(
                articles,
                many=True,
                context={'request': request}).data
        })


class Bookmarkarticle(
        generics.ListAPIView,
        generics.CreateAPIView,
        generics.DestroyAPIView):
    """
        view used to create & delete bookmarks
    """
    lookup_field = "slug"
    queryset = Bookmarks.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = BookmarkSerializer

    def get(self, request, slug, *args, **kwargs):
        """
            list all article bookmarkers
        """
        try:

            article = Articles.objects.get(
                slug__iexact=slug)

        except Articles.DoesNotExist:
            return Response(data={
                "error":
                "Article ({}) does not exist.".format(slug)},
                status=status.HTTP_404_NOT_FOUND)

        bookmarkers = Bookmarks.objects.filter(article=article)

        return Response(data={
            "bookmarkers": ListBookmarkersSerializer(
                bookmarkers,
                many=True,
                context={'request': request}).data
        })

    def post(self, request, slug, *args, **kwargs):
        """
            create bookmark
        """
        try:

            article = Articles.objects.get(
                slug__iexact=slug)

        except Articles.DoesNotExist:
            return Response(data={
                "error":
                "Article ({}) does not exist.".format(slug)},
                status=status.HTTP_404_NOT_FOUND)
        data = {
        }

        serializer = self.serializer_class(
            data=data
        )
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save(article=article, user=self.request.user)
        except IntegrityError:
            return Response(data={
                "error": "You already bookmarked {}".format(article.title)
            }, status=status.HTTP_409_CONFLICT)
        return Response(data={
            "data": "You have successfully bookmarked {}".format(article.title)
        }, status=status.HTTP_201_CREATED)

    def delete(self, request, slug, *args, **kwargs):
        """
            unbookmarking an article
        """
        try:

            article = Articles.objects.get(
                slug__iexact=slug)

        except Articles.DoesNotExist:
            return Response(data={
                "error":
                "Article ({}) does not exist.".format(slug)},
                status=status.HTTP_404_NOT_FOUND)

        try:
            bookmark = Bookmarks.objects.get(
                article=article,
                user=self.request.user)
            bookmark.delete()
            return Response(data={
                "data":
                    "You have successfully unbookmarked {}".format(
                        article.title)
            })
        except Bookmarks.DoesNotExist:
            return Response(data={
                "error":
                "You had not bookmarked {}".format(article.title)
            }, status=status.HTTP_404_NOT_FOUND)
