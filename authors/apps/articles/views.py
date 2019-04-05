from rest_framework.generics import (CreateAPIView,
                                     ListAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.response import Response
from rest_framework import status, pagination
from rest_framework.pagination import PageNumberPagination
from .models import Articles
from .serializers import ArticlesSerializer, LikesSerializer
from ..authentication.models import User
from .models import Articles, Likes
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from django.contrib.contenttypes.models import ContentType
from .serializers import ArticlesSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .models import Rating
from .serializers import RatingSerializer

from rest_framework.renderers import JSONRenderer


class ArticlesPagination(PageNumberPagination):
    page_size_query_param = 'page_size'


class CreateArticleView(CreateAPIView, ListAPIView, PageNumberPagination):
    queryset = Articles.objects.get_queryset().order_by('id')
    ordering = ['-id']
    serializer_class = ArticlesSerializer
    pagination_class = ArticlesPagination

    def post(self, request):
        if request.user.is_authenticated:
            article = request.data.get('article', {})
            serializer = self.serializer_class(
                data=article
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(author=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {
                    "status": 403,
                    "error": "Please login"
                }, status=status.HTTP_403_FORBIDDEN
            )

    def get(self, request, *args, **kwargs):

        page_size = request.GET.get('page_size')
        if page_size is None:
            page_size = 10

        pagination.PageNumberPagination.page_size = page_size

        return self.list(request, *args, **kwargs)


class SingleArticleView(RetrieveUpdateDestroyAPIView):
    lookup_field = 'slug'
    queryset = Articles.objects.all()
    serializer_class = ArticlesSerializer

    def put(self, request, slug, *args, **kwargs):

        article = get_object_or_404(Articles, slug=slug)
        if article.author.id != request.user.id:
            data = {'error':
                    'You are not allowed to edit this article'}

            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.serializer_class(
            instance=article, data=request.data, partial=True
        )
        serializer.is_valid()
        serializer.save()
        return Response({'article': serializer.data},
                        status=status.HTTP_200_OK)

    def delete(self, request, slug, *args, **kwargs):
        article = get_object_or_404(Articles, slug=slug)
        if article.author.id != request.user.id:
            data = {'error':
                    'You are not allowed to delete this article'}

            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        return self.destroy(request, *args, **kwargs)


class RatingView(CreateAPIView, ListAPIView):
    lookup_field = 'article_id'
    permission_classes = (IsAuthenticated,)
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def post(self, request, article_id, *args, **kwargs):
        rating = get_object_or_404(Articles, id=article_id)
        if request.user.is_authenticated:
            rating = request.data.get('rating', {})
            user_id = {"user_id": request.user.id}
            rating.update(user_id)
            article_id = {"article_id": article_id}
            rating.update(article_id)
            serializer = self.serializer_class(
                data=rating
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {
                    "status": 403,
                    "error": "Please login"
                }, status=status.HTTP_403_FORBIDDEN
            )


class LikeView(APIView):

    """creating and updating likes
    """
    permission_classes = (IsAuthenticated,)
    queryset = None
    serializer_class = LikesSerializer

    def post(self, request, slug, *args, **kwargs):
        """Like
        Arguments:
            request {[type]} -- [description]
            slug {[type]} -- [description]
        """
        actions = {'like': 1, 'dislike': -1}
        data = request.data
        data['user'] = request.user.id

        action = data.get('action', None)
        if not action:
            return Response({'Errors': 'Action not found'},
                            status=status.HTTP_400_BAD_REQUEST)

        article = get_object_or_404(Articles, slug=slug)
        article_id = article.pk

        actiondb = actions.get(action, 0)
        updatefields = {'like': actiondb}
        likeDict = dict(user=request.user,
                        article=article, like=actiondb)

        try:
            like = Likes.objects.get(
                user=request.user, article=article)
            like.like = actiondb
            like.save()
        except Likes.DoesNotExist:
            like = Likes(**likeDict)
            like.save()
        except IntegrityError:
            return Response({'Errors': 'Something went wrong'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        articleS = ArticlesSerializer(instance=article)
        count = self.countLikes(article_id)
        return Response(count, status=status.HTTP_200_OK)

    def get(self, request, slug, type=None, *args, **kwargs):
        article = get_object_or_404(Articles, slug=slug)
        article_id = article.pk

        count = self.countLikes(article_id)
        if type == 'count':

            return Response(count, status=status.HTTP_200_OK)

        l_serialize = LikesSerializer(self.l_queryset, many=True)
        d_serialize = LikesSerializer(self.d_queryset, many=True)
        import json
        likes = json.loads(JSONRenderer().render(l_serialize.data))
        dislikes = json.loads(JSONRenderer().render(d_serialize.data))
        print(dislikes)

        likesDict = {'likes': likes, 'dislikes': dislikes, 'count': count
                     }
        return Response(likesDict, status=status.HTTP_200_OK)

    def delete(self, request, slug, *args, **kwargs):

        article = get_object_or_404(Articles, slug=slug)
        article_id = article.pk
        try:
            like = Likes.objects.get(
                user=request.user, article=article)
            like.delete()
        except Likes.DoesNotExist:
            return Response({'Errors': 'You have not liked this Article'},
                            status=status.HTTP_404_NOT_FOUND)

        count = self.countLikes(article_id)
        return Response(count, status=status.HTTP_200_OK)

    def countLikes(self, article_id):
        self.l_queryset = Likes.objects.likes().filter(article=article_id)
        self.d_queryset = Likes.objects.dislikes().filter(article=article_id)
        likesCount = self.l_queryset.count()
        dislikesCount = self.d_queryset.count()
        count = {'likes': likesCount,
                 'dislikes': dislikesCount,
                 'total': likesCount+dislikesCount}
        return count
