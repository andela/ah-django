from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions

from authors.apps.stats.models import ReadStats
from .serializers import ReaderStatsSerialer
from .renderers import ReaderStatsRenderer


class ReaderStatsApiView(generics.ListAPIView):
    """
        Handles requests to for the user stats
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = ReaderStatsSerialer
    renderer_classes = (ReaderStatsRenderer, )

    def get(self, request, **kwargs):
        """
            Fetches all statistics of a particular reader
        """
        if kwargs.get('username') != request.user.username:
            raise exceptions.PermissionDenied(
                'You have no permission to perform this action')
        user_stats = ReadStats.objects.filter(user=request.user)
        data = self.serializer_class(user_stats, many=True).data
        return Response(data=data,
                        status=status.HTTP_200_OK)
