from rest_framework import generics, status, exceptions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import HighlightSerializer
from .renderers import RenderHighlights
from .models import Highlight
from ..articles.models import Article


def article_exists(article_slug):
    try:
            # Check if an article with that slug exists
        return Article.objects.get(slug=article_slug)
    except Article.DoesNotExist:
        raise exceptions.NotFound


def highlight_exists(highlight_id):
    try:
        return Highlight.objects.get(id=highlight_id)
    except Highlight.DoesNotExist:
        raise exceptions.NotFound


class HighlightApiList(generics.ListCreateAPIView):
    """
    Defines views for creating a highlight
    """
    permission_classes = (IsAuthenticated,)
    renderer_classes = (RenderHighlights,)
    serializer_class = HighlightSerializer
    queryset = Highlight.objects.all()

    def post(self, request, slug):
        """Creates a highlight

        Adds a highlight to an article
         """
        article = article_exists(slug)

        highlight_object = request.data.get('highlight_object', {})
        serializer = self.serializer_class(data=highlight_object)
        serializer.is_valid(raise_exception=True)

        if highlight_object['highlight'] in article.body:
            if not Highlight.objects.filter(
                    highlight=highlight_object['highlight']).exists():
                serializer.save(
                    highlighter=request.user,
                    article_id=article.id,
                    highlight=highlight_object['highlight'],
                    comment=highlight_object['comment']
                )
                return Response(
                    data=serializer.data,
                    status=status.HTTP_201_CREATED
                )
            return Response(
                data={
                    "highlight": "You seem to have a similar text highlighted already\
                    consider updating the comment instead"
                },
                status=status.HTTP_409_CONFLICT
            )

        return Response(
            data={
                "highlight": "Your highlight has to be within the article"
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    def list(self, request, slug):
        """List highlights

        Return all highlights from the system
        """

        article = article_exists(slug)
        filtered_queryset = self.get_queryset().filter(
            highlighter=request.user,
            article=article.id)
        serializer = self.serializer_class(filtered_queryset, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class HighlightApiView(generics.RetrieveUpdateDestroyAPIView):
    """
    Peforms actions on a single highlight
    """

    permission_classes = (IsAuthenticated,)
    renderer_classes = (RenderHighlights,)
    serializer_class = HighlightSerializer
    queryset = Highlight.objects.all()

    def get(self, request, slug, highlight_id):
        """Retrieves a single highlight

        Returns a given highlight object
        """
        article_exists(slug)
        highlight = highlight_exists(highlight_id)
        filtered_queryset = self.get_queryset().filter(
            id=highlight.id,
            highlighter=request.user
        )

        serializer = self.serializer_class(filtered_queryset, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def destroy(self, request, slug, highlight_id):
        """ deletes a highlight """

        article_exists(slug)
        highlight_exists(highlight_id)

        Highlight.objects.filter(id=highlight_id).delete()

        return Response(data={
            "message": "Successfully deleted the highlight"
        }, status=status.HTTP_200_OK)
