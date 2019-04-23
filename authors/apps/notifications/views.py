from rest_framework.response import (Response)
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import (
    IsAuthenticated)

from authors.apps.authentication.models import User


class NotificationView(APIView):
    lookup_field = "type"
    permission_classes = (IsAuthenticated,)

    def post(self, request, type, *args, **kwargs):
        if type not in ["email", "in_app"]:
            return Response(data={
                "error": "The type should either be (email) or (in_app)"
            }, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(username=request.user.username)
        if type == "email":
            if user.email_notifications is True:
                return Response(data={
                    "error":
                    "You are already opted into email notifications"
                }, status=status.HTTP_409_CONFLICT)
            user.email_notifications = True
            user.save()
            return Response(data={
                "data": "You have opted into email notifications"},
                status=status.HTTP_200_OK)

        if type == "in_app":
            if user.in_app_notifications is True:
                return Response(data={
                    "error":
                    "You are already opted into in_app notifications"
                }, status=status.HTTP_409_CONFLICT)
            user.in_app_notifications = True
            user.save()
            return Response(data={
                "data": "You have opted into in_app notifications"},
                status=status.HTTP_200_OK)

    def delete(self, request, type, *args, **kwargs):
        if type not in ["email", "in_app"]:
            return Response(data={
                "error": "The type should either be (email) or (in_app)"
            }, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(username=request.user.username)
        if type == "email":
            if user.email_notifications is False:
                return Response(data={
                    "error":
                    "You are already opted out of email notifications"
                }, status=status.HTTP_409_CONFLICT)
            user.email_notifications = False
            user.save()
            return Response(data={
                "data": "You have opted out of email notifications"},
                status=status.HTTP_200_OK)

        if type == "in_app":
            if user.in_app_notifications is False:
                return Response(data={
                    "error":
                    "You are already opted out of in_app notifications"
                }, status=status.HTTP_409_CONFLICT)
            user.in_app_notifications = False
            user.save()
            return Response(data={
                "data": "You have opted out of in_app notifications"},
                status=status.HTTP_200_OK)
