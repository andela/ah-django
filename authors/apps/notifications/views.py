""" This module defines views for notifications """
from notifications.models import Notification
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from ..notifications.serializers import NotififcaionSerializers
from ..notifications.renderers import NotificationJSONRenderer


class NotificationListViews(APIView):
    """Unread notifications
    Retrieve unread notifications
     """

    permission_classes = (IsAuthenticated,)
    serializer_class = NotififcaionSerializers
    renderer_classes = (NotificationJSONRenderer,)

    def get(self, request):
        """ retrieves """

        user = request.user
        notifications = user.notifications.unread()
        serializer = self.serializer_class(notifications, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request, format=None):
        """ Mark as unread """
        user = request.user
        Notification.objects.mark_all_as_unread(user)
        return Response({
            "response": "All unread"
        }, status.HTTP_200_OK)


class ReadNotificationApiView(APIView):
    """
    Retrieves read notifications
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = NotififcaionSerializers
    renderer_classes = (NotificationJSONRenderer,)

    def get(self, request):
        """Read notifications
        Retrieves read notifications
        """
        user = request.user
        notifications = user.notifications.read()
        serializer = self.serializer_class(notifications, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request, format=None):
        """ Mark as read """
        user = request.user
        Notification.objects.mark_all_as_read(user)
        return Response({
            "response": "All read"
        }, status.HTTP_200_OK)


class ReadUpdateDeleteApiView(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = NotififcaionSerializers
    renderer_classes = (NotificationJSONRenderer,)

    def get(self, request, pk, format=None):
        """Retrieves one notification  """
        user = request.user
        notification = user.notifications.filter(id=pk)

        return Response(self.serializer_class(
            notification, many=True).data, status.HTTP_200_OK)
