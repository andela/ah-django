from rest_framework.generics import (CreateAPIView, RetrieveAPIView,
                                     ListAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.response import Response
from rest_framework import status
from .models import Comments
from ..articles.models import Articles
from .serializers import (CommentsSerializer, CommentHistorySerializer)
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


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
