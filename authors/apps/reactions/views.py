from django.contrib.contenttypes.models import ContentType

from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import exceptions

from .serializers import ReactionSerializer
from .models import UserReaction
from .renderers import ReactionRenderer
from authors.apps.articles.models import Article
from authors.apps.comments.views import CommentAPIView, ArticleInst
from .helpers import dislikeReaction


class UserReactionView(CreateAPIView):
    """
        Allows user to post reactions to an
        article
    """
    serializer = ReactionSerializer
    reaction = None
    model = None
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (ReactionRenderer,)

    def post(self, request, slug):
        """
            Posts a like or dislike to an article
            from an autheticated user.
        """
        expressed_article = self.get_article(slug)
        response, status_ = dislikeReaction.mofidy_reaction(
            expressed_article,
            request.user,
            self.reaction,
            'article')

        return Response(
            response,
            status=status_)

    def get_article(self, art):
        """
            Fetches and returns an article instance
            given its slug field
        """
        try:
            article = Article.objects.get(slug=art)
        except Exception as ex:
            print(ex)
            raise exceptions.NotFound(f'Article of title {art} seems missing')
        else:
            return article


class CommentsLikeReactionAPIView(CreateAPIView):
    """
        Handles posting of likes and dislikes to
        comments
    """
    serializer = ReactionSerializer
    reaction = None
    model = None
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (ReactionRenderer,)

    def post(self, request, slug, id):
        article = ArticleInst.fetch(slug)
        comment = CommentAPIView.check_comment(id, article)

        data, status_ = dislikeReaction.mofidy_reaction(
            instance=comment,
            user=request.user,
            inherited_react=self.reaction,
            name='comment'
        )

        return Response(data=data,
                        status=status_)
