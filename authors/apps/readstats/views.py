from .models import ReadStats
from ..authentication.models import User
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from .serializers import (UserStatsSerializer,
                          ArticleStatsSerializer,
                          AdminStatsSerializer)
from rest_framework.response import (Response)
from rest_framework import status
from ..articles.models import Articles
from django.db.models import Sum
# Create your views here.


class UserStatsView(APIView):
    """
        A user should be view his/her own read stats
    """
    lookup_field = 'username'
    permission_classes = (IsAuthenticated,)
    serializer_class = UserStatsSerializer

    def get(self, request, *args, **kwargs):
        # Save read status

        stats = ReadStats.objects.filter(user=request.user)

        if stats:
            serializer = UserStatsSerializer(stats, many=True)
            return Response(
                {
                    "total_reads": len(stats),
                    "stats": serializer.data
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    "status": 404,
                    "error": "No stats available"
                }, status=status.HTTP_404_NOT_FOUND
            )


class ArticStatsView(APIView):
    """
        A user should be view his/her own read stats
    """
    lookup_field = 'slug'
    permission_classes = (IsAuthenticated,)
    serializer_class = ArticleStatsSerializer

    def get(self, request, slug, *args, **kwargs):

        try:

            article = Articles.objects.get(slug=slug)

            if article.author == request.user:

                stats = ReadStats.objects.filter(article=article)

                if stats:
                    serializer = ArticleStatsSerializer(stats, many=True)
                    return Response(
                        {
                            "total_views":
                            stats.aggregate(Sum('views'))['views__sum'],
                            "stats": serializer.data
                        },
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {
                            "status": 404,
                            "error":
                            "{} does not have any stats".format(article.title)
                        }, status=status.HTTP_404_NOT_FOUND
                    )

            else:
                return Response(
                    {
                        "status": 403,
                        "error": "Not allowed"
                    }, status=status.HTTP_403_FORBIDDEN
                )

        except Articles.DoesNotExist:
            return Response(
                {
                    "status": 404,
                    "error": "Article not found"
                }, status=status.HTTP_404_NOT_FOUND
            )


class AdminStatsView(APIView):
    """
        A user should be view his/her own read stats
    """
    permission_classes = (IsAdminUser,)
    serializer_class = AdminStatsSerializer

    def get_queryset(self):
        queryset = ReadStats.objects.all()
        username = self.request.query_params.get('username', None)
        article = self.request.query_params.get('article', None)
        ascendingviews = self.request.query_params.get('asc_views', None)
        descendingviews = self.request.query_params.get('desc_views', None)

        # search
        if username is not None:
            queryset = queryset.filter(user__username__icontains=username)
        if article is not None:
            queryset = queryset.filter(article__title__icontains=article)
        # ascending&descending
        if ascendingviews is not None:
            queryset = queryset.order_by('views')
        else:
            if descendingviews is not None:
                queryset = queryset.order_by('-views')

        return queryset

    def get(self, request, *args, **kwargs):

        stats = self.get_queryset()

        if stats:
            serializer = AdminStatsSerializer(stats, many=True)
            return Response(
                {
                    "stats": serializer.data
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    "status": 404,
                    "error": "No stats available"
                }, status=status.HTTP_404_NOT_FOUND
            )
