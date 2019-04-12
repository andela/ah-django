from rest_framework.generics import ListAPIView
from .serializers import BookmarkSerializer
from authors.apps.articles.models import Article
from .models import BookmarkArticle
from rest_framework.response import Response
from rest_framework import status
from rest_framework import exceptions, generics


class BookmarkAPIView(generics.GenericAPIView):
    """ Bookmark togggle to mark and unmark article"""
    serializer_class = BookmarkSerializer

    def post(self, request, slug):
        """ method to verify bookmark status """
        user = request.user
        try:
            _article = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise exceptions.NotFound(f'Article with slug {slug} nonexistent')

        bookmark, created = BookmarkArticle.objects.get_or_create(
            user=user,
            _article=_article
        )

        return Response(
            {
                'message': 'Article succesfully BOOKMARKED',
            }, status=status.HTTP_201_CREATED,
        )

    def delete(self, request, slug):
        """ method to unbookmark article """
        user = request.user
        try:
            _article = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise exceptions.NotFound(f'Article with slug {slug} nonexistent')
        bookmark, created = BookmarkArticle.objects.get_or_create(
            user=user,
            _article=_article
        )
        bookmark.delete()

        return Response(
            {
                'message': 'Bookmark succesfully DELETED',
            }, status.HTTP_200_OK

        )


class BookmarkListAPIView(ListAPIView):
    """ Retrieve all bookmarked articles"""

    def list(self, request):
        """ method to verify bookmark status """
        queryset = BookmarkArticle.objects.select_related(
            '_article', 'user'
        ).filter(user=request.user)

        serializer = BookmarkSerializer(queryset, many=True)

        return Response({
            'bookmarked articles': serializer.data,
            'count': len(serializer.data)
        }, status=status.HTTP_201_CREATED,
        ) if len(serializer.data) else \
            Response({
                'message': 'NO article Bookmarked',
            }, status.HTTP_200_OK)
