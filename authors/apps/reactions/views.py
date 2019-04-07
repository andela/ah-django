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
        try:
            like_status = UserReaction.objects.get(
                content_type=ContentType.objects.get_for_model(
                    expressed_article),
                object_id=expressed_article.id,
                user=request.user
            )
            status_ = status.HTTP_200_OK

            if like_status.user_reaction is not self.reaction:
                like_status.user_reaction = self.reaction
                like_status.save(update_fields=['user_reaction'])
                msg = 'Reaction changed'
            else:
                like_status.delete()
                msg = 'Reaction Removed'
        except UserReaction.DoesNotExist:
            expressed_article.user_reaction.create(
                user_reaction=self.reaction,
                user=request.user)
            msg = "Reaction Created"
            status_ = status.HTTP_201_CREATED

        response = {'message': msg}
        data = {
            'article': slug,
            'likes': expressed_article.
            user_reaction.likes.count(),
            'dislikes': expressed_article.
            user_reaction.dislikes.count(),
            'participated_users': expressed_article.
            user_reaction.fetch_popularity_status()
        }
        response['data'] = data

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
