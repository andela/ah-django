from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.generics import (CreateAPIView, RetrieveAPIView,
                                     ListAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.response import Response
from rest_framework import status
from .models import Comments, Like
from ..articles.models import Articles
from .serializers import (CommentsSerializer,
                          CommentHistorySerializer, CommentsLikesSerializer)
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from datetime import datetime
from rest_framework.renderers import JSONRenderer
import json


class CreateCommentView(CreateAPIView, ListAPIView):
    '''Endpoint for creating a comments'''
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    lookup_field = 'article_slug'
    permission_classes = (IsAuthenticated,)

    def post(self, request, article_slug):
        '''Handles all post requests to create a comment'''

        if Articles.objects.filter(slug=article_slug).exists():
            # check if user is authorized
            comment = request.data.get('comment', {})
            article = Articles.objects.filter(slug=article_slug).first()
            comment.update({'article': article})

            serializer = self.serializer_class(data=comment)
            serializer.is_valid(raise_exception=True)
            highlighted_text = comment.get('highlighted_text', None)
            serializer.val_highlighted_text(highlighted_text, article)
            comment['user'] = request.user
            comment_ob = Comments(**comment)
            comment_ob.save()
            serializer = self.serializer_class(instance=comment_ob)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Article does not exist"},
                            status=status.HTTP_404_NOT_FOUND)

    def get(self, request, article_slug):
        '''Handles all get requests by users to view the
           comments of a particular article
        '''
        article = get_object_or_404(Articles, slug=article_slug)
        queryset = self.get_queryset().filter(article=article)
        serializer = CommentsSerializer(
            queryset, many=True, context={'request': request})

        count = len(serializer.data)

        if count > 0:
            return Response({"Comments": serializer.data,
                             "Count": count},
                            status=status.HTTP_200_OK)
        else:
            return Response({"error": "Article has no comments"},
                            status=status.HTTP_204_NO_CONTENT)


class UpdateDeleteCommentView(RetrieveUpdateDestroyAPIView):
    '''Handles all requests for updating and deleting requests'''
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    lookup_field = 'id'
    permission_classes = (IsAuthenticated,)

    def put(self, request, article_slug, id):
        '''Handles all requests by user to update their comments'''
        article = get_object_or_404(Articles, slug=article_slug)
        comments = get_object_or_404(Comments, id=id, article=article)
        comment = Comments.objects.get(id=id)
        if comment.user != request.user:
            data = {'error':
                    'You are not allowed to edit this  comment'}

            return Response(data, status=status.HTTP_403_FORBIDDEN)
        comm = request.data.get('comment', {})

        serializer = self.serializer_class(
            instance=comment, data=comm,
        )
        serializer.is_valid(raise_exception=True)
        highlighted_text = comm.get('highlighted_text', None)
        serializer.val_highlighted_text(highlighted_text, article)
        serializer.save()
        return Response({'Comment': serializer.data},
                        status=status.HTTP_200_OK)

    def delete(self, request, article_slug, id):
        '''handles all requests for uses to delete their comments'''
        if Articles.objects.filter(slug=article_slug).exists():
            article = Articles.objects.get(slug=article_slug)
            comments = get_object_or_404(Comments, id=id, article=article)
            comment = Comments.objects.filter(id=id).first()
            if comment.user == request.user:
                comment = Comments.objects.get(id=id)
                comment.delete()
                return Response({"Message": "Comment deleted"},
                                status=status.HTTP_200_OK)
            else:
                return Response({"error":
                                 "You cannot delete this comment"},
                                status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"error": "Article does not exist"},
                            status=status.HTTP_404_NOT_FOUND)


class CommentHistoryView(RetrieveAPIView):
    '''View class used to retrieve history
       of a specific comment.
    '''
    queryset = Comments.objects.all()
    serializer_class = CommentHistorySerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        '''get edit history of a comment'''

        comment = get_object_or_404(Comments, id=id)
        serializer = self.serializer_class(comment)

        return Response(serializer.data, status=status.HTTP_200_OK)


class LikeView(CreateAPIView):
    """
    LIke commet CRUD operations
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentsLikesSerializer

    def counter(self, id):
        likes_queryset = Like.objects.likes().filter(comment=id)
        dislikes_queryset = Like.objects.dislikes().filter(comment=id)
        likesCount = likes_queryset.count()
        dislikesCount = dislikes_queryset.count()
        count = {'likes': likesCount,
                 'dislikes': dislikesCount,
                 'total': likesCount+dislikesCount}
        return count
    # swagger docs code
    action_props = {"action": {"type": "string"}}
    action_schema = openapi.Schema(
        title='likes', description="Actions", properties=action_props,
        type=openapi.TYPE_OBJECT)

    @swagger_auto_schema(request_body=action_schema,
                         operation_description="Like, dislike a Comment ",
                         )  # end swagger docs code
    def post(self, request, id):
        """
        Post a like/dislike
        """
        actions = {
            'like': 1,
            'dislike': -1
        }
        data = request.data
        action = data.get('action', None)
        if not action:
            return Response({'error': 'Please provide an action'},
                            status=status.HTTP_400_BAD_REQUEST)

        comment = get_object_or_404(Comments, id=id)
        user = self.request.user
        actiondb = actions.get(action, 0)
        like = {'like': actiondb}
        try:
            queryset = Like.objects.get(
                user=user, comment=comment
            )
            queryset.updated_at = datetime.now()
            queryset.like = actiondb
            queryset.save()
        except Like.DoesNotExist:
            serializer = self.serializer_class(
                data=like
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(comment=comment, user=user)
        counter = self.counter(id)
        return Response(counter,
                        status=status.HTTP_200_OK)

    def get(self, request, id):
        get_object_or_404(Comments, id=id)

        counter = self.counter(id)
        likes_queryset = Like.objects.likes().filter(comment=id)
        dislikes_queryset = Like.objects.dislikes().filter(comment=id)

        l_serialize = self.serializer_class(likes_queryset, many=True)
        d_serialize = self.serializer_class(dislikes_queryset, many=True)

        likes = json.loads(JSONRenderer().render(l_serialize.data))
        dislikes = json.loads(JSONRenderer().render(d_serialize.data))

        likes = {'likes': likes,
                 'dislikes': dislikes,
                 'count': counter}
        return Response(likes, status=status.HTTP_200_OK)

    def delete(self, request, id):
        try:
            like = Like.objects.get(user=request.user, comment=id)
            like.delete()

            return Response({
                "message": "Comment like has been deleted"
            }, status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            return Response({
                "error": "You have not liked this comment"
            }, status=status.HTTP_404_NOT_FOUND)
