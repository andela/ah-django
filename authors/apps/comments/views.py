from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from rest_framework import exceptions

from authors.apps.articles.models import Article
from .serializers import CommentSerializer, CommentReplySerializer
from .renderers import CommentRenderer, CommentReplyRenderer
from .models import Comment, CommentReply
from ..core.permissions import IsOwnerOrReadOnly


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
            raise exceptions.NotFound(f'Article of slug {slug} nonexistent')
        else:
            return article


class ListCommentsView(generics.ListCreateAPIView):
    """
        Handles listing of all comments and creation of new comments
        to an article
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = CommentSerializer
    renderer_classes = (CommentRenderer,)

    def post(self, request, slug):
        """
            Posts a comment to an article
        """
        article = ArticleInst.fetch(slug)
        comment = request.data.get('comment', {})

        serializer = self.serializer_class(data=comment)
        serializer.is_valid(raise_exception=True)
        status_ = status.HTTP_201_CREATED

        try:
            Comment.objects.get(
                article=article,
                body=comment.get('body')
            )
        except Comment.DoesNotExist:
            serializer.save(author=request.user, article=article)
            resp = {'message': 'Comment created'}
            resp['data'] = serializer.data

        else:
            resp = {'message': "Seems you've posted an exact comment before"}
            status_ = status.HTTP_409_CONFLICT
        return Response(data=resp,
                        status=status_
                        )

    def get(self, request, slug):
        """
            Retrieves all comments associated with
            an article
        """
        article = ArticleInst.fetch(slug)

        comments = Comment.objects.filter(article=article)
        serializer = self.serializer_class(comments, many=True)

        response = {'data': serializer.data}
        response.update(
            {'comments count': comments.count()}
        )
        return Response(data=response, status=status.HTTP_200_OK)


class CommentAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
        Creates, Updates and Deletes a single comment
    """
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    renderer_classes = (CommentRenderer,)
    serializer_class = CommentSerializer

    def get(self, request, slug, id):
        """
            Fetches a comment on an article
        """
        article = ArticleInst.fetch(slug)

        try:
            comment = Comment.objects.get(pk=id, article=article)
        except Comment.DoesNotExist:
            data = {
                'error': f'Comment of ID {id} nonexistent'
            }
            status_ = status.HTTP_404_NOT_FOUND
        else:
            serializer = self.serializer_class(comment)
            status_ = status.HTTP_200_OK
            data = serializer.data
        return Response(
            data=data,
            status=status_)

    def update(self, request, slug, id):
        """
            Updates an existing comment
        """
        article = ArticleInst.fetch(slug)
        updated_comment = request.data.get('comment', {})
        comment = self.check_comment(id, article)

        similar_comment = Comment.objects.filter(
            article=article,
            body=updated_comment.get('body')
        )

        if similar_comment:
            data = {'message': "You've posted a similar comment before"}
            status_ = status.HTTP_409_CONFLICT
        else:
            response = {'message': 'Comment Updated'}
            response['data'] = updated_comment
            serializer = self.serializer_class(
                comment,
                data=updated_comment,
                partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            data = serializer.data
            status_ = status.HTTP_200_OK

        return Response(data=data, status=status_)

    def destroy(self, request, slug, id):
        """
            Removes a comment from an article
        """
        article = ArticleInst.fetch(slug)
        comment = self.check_comment(key=id, article=article)
        comment.delete()

        return Response(
            {'message': f'Comment of ID {id} deleted'},
            status=status.HTTP_200_OK
        )

    @classmethod
    def check_comment(cls, key, article):
        """
            Queries for an existing comment object
        """

        try:
            comment = Comment.objects.get(pk=key, article=article)
        except Comment.DoesNotExist:
            raise exceptions.NotFound(f'Comment of ID {key} nonexistent')

        return comment


class ReplyList(generics.ListCreateAPIView):
    """
        Handles viweing of replies made to a comment
        and replying to an article comment
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = CommentReplySerializer
    renderer_classes = (CommentReplyRenderer,)
    lookup_field = 'comment_to'
    queryset = CommentReply.objects.all()

    def post(self, request, slug, id):
        """
            Posts a reply to a comment
        """
        article = ArticleInst.fetch(slug)
        comment = request.data.get('comment', {})
        posted_comment = CommentAPIView.check_comment(
            id, article)

        serializer = self.serializer_class(data=comment)
        serializer.is_valid(raise_exception=True)
        status_ = status.HTTP_201_CREATED

        try:
            CommentReply.objects.get(
                comment_to=posted_comment,
                author=request.user,
                body=comment.get('body').strip()
            )
        except CommentReply.DoesNotExist:
            serializer.save(author=request.user,
                            article=article,
                            comment_to=posted_comment)
            resp = {'message': f'Replied to comment of ID {id}'}
            resp['data'] = serializer.data

        else:
            resp = {'message': "Seems you've posted an exact comment before"}
            status_ = status.HTTP_409_CONFLICT
        return Response(data=resp,
                        status=status_
                        )

    def get(self, request, slug, id):
        """
            Retrieves all replies to a comment
            of matching ID
        """
        article = ArticleInst.fetch(slug)

        posted_comment = CommentAPIView.check_comment(
            article=article,
            key=id)

        comments = posted_comment.replies

        response = {'comment': posted_comment.body}
        response['replies'] = comments
        response.update(
            {'replies count': len(comments)}
        )
        return Response(data=response, status=status.HTTP_200_OK)


class ReplyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
        Creates, Updates and Deletes a single reply
        to an article comment
    """
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    renderer_classes = (CommentReplyRenderer,)
    serializer_class = CommentReplySerializer

    def get(self, request, slug, id, key):
        """
            Fetches a comment on an article
        """
        article = ArticleInst.fetch(slug)
        CommentAPIView.check_comment(article=article, key=id)

        comment_reply = self.get_reply(parent=id, child=key)
        serializer = self.serializer_class(comment_reply)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK)

    def update(self, request, slug, id, key):
        """
            Updates a reply to a comment
        """
        article = ArticleInst.fetch(slug)
        updated_reply = request.data.get('comment', {})
        parent = CommentAPIView.check_comment(id, article)
        comment = self.get_reply(parent=parent, child=key)

        similar_comment = CommentReply.objects.filter(
            comment_to=parent,
            body=updated_reply.get('body')
        )

        if similar_comment:
            data = {'message': "You've posted a similar comment before"}
            status_ = status.HTTP_409_CONFLICT
        else:
            response = {'message': 'Comment Updated'}
            response['data'] = updated_reply
            serializer = self.serializer_class(
                comment,
                data=updated_reply,
                partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            data = serializer.data
            status_ = status.HTTP_200_OK

        return Response(data=data, status=status_)

    def destroy(self, request, slug, id, key):
        """
            Removes a reply from a comment
        """
        article = ArticleInst.fetch(slug)
        parent = CommentAPIView.check_comment(id, article)
        reply = self.get_reply(parent=parent, child=key)
        reply.delete()

        return Response(
            {'message': f'Comment Reply of ID {key} deleted'},
            status=status.HTTP_200_OK
        )

    def get_reply(self, parent, child):
        """
            Queries for a reply to a comment using the
            reply's primary key and the comment foreign key
        """
        try:
            reply = CommentReply.objects.get(
                pk=child,
                comment_to=parent)
        except CommentReply.DoesNotExist:
            raise exceptions.NotFound(
                f'Comment reply of ID {child} nonexistent'
            )

        return reply
