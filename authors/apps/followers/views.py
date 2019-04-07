from .models import Follow
from authors.apps.core.permissions import IsOwnerOrReadOnly
from authors.apps.authentication.models import User
from rest_framework.generics import (
    ListCreateAPIView, DestroyAPIView)
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated)
from .serializers import (FollowSerializer,
                          FollowerSerializer,
                          FollowerListSerializer)
from rest_framework.exceptions import ValidationError
from .renderers import FollowerJsonRenderer, FollowerListJsonRenderer
from rest_framework import status
from rest_framework.response import Response


def user_not_found():
    raise ValidationError(
        {'error': 'User with that username not found'})


class ListCreateFollow(ListCreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    renderer_classes = (FollowerJsonRenderer,)

    def post(self, request, username):
        """
        A method for following a user
        """
        user_exists = User.objects.filter(username=username).exists()
        if not user_exists:
            return Response(
                {'error': 'user with that name was not found'},
                status.HTTP_404_NOT_FOUND)
        # we check if the user is already followed
        followed_user = User.objects.get(username=username)
        already_followed = Follow.is_user_already_followed(
            followed_user_id=followed_user.id,
            user_id=self.request.user.id
        )
        if already_followed:
            return Response({'error': 'user already followed'},
                            status.HTTP_400_BAD_REQUEST)
        if followed_user.id == self.request.user.id:
            return Response({'error': "you cannot follow yourself."},
                            status.HTTP_400_BAD_REQUEST)
        data = {
            "followed_user": followed_user.id,
            "user": self.request.user.id}
        serializer = FollowSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'message': 'user followed successfully'},
                        status.HTTP_201_CREATED)


class FollowersView(ListCreateAPIView):
    """
    Enable user view a list of follwers
    """
    queryset = Follow.objects.all()
    serializer_class = FollowerListSerializer
    permission_classes = (IsAuthenticated,)
    renderer_classes = (FollowerListJsonRenderer,)

    def get(self, request, **kwargs):
        username = kwargs.get('username')
        user = User.objects.filter(username=username).first()
        if not user:
            user_not_found()
        queryset = Follow.objects.filter(followed_user=user)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteFollower(DestroyAPIView):
    """
    This is for unfollowing a user
    """
    queryset = Follow.objects.all()
    serializer_class = FollowerSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def delete(self, request, username):
        """
        Removes a user from following list
        """
        followed_user_exists = User.objects.filter(username=username).exists()
        if not followed_user_exists:
            return Response({'error': 'user not found'},
                            status.HTTP_404_NOT_FOUND)
        followed_user = User.objects.get(username=username)
        user_exists = Follow.is_user_already_followed(
            followed_user_id=followed_user.id,
            user_id=request.user.id
        )
        if user_exists:
            instance = Follow.objects.filter(
                user=self.request.user.id, followed_user=followed_user.id
            )
            instance.delete()
            return Response({'message': 'user unfollowed'},
                            status.HTTP_200_OK)
        return Response({'message': 'user not in followers'},
                        status.HTTP_404_NOT_FOUND)


class RetrieveFollowing(ListCreateAPIView):
    """
    A user is able to see the people they are following
    """

    queryset = Follow.objects.all()
    serializer_class = FollowerSerializer
    renderer_classes = (FollowerJsonRenderer,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, **kwargs):
        username = kwargs.get('username')
        """
        Get userlist by using the username value
        """
        user = User.objects.filter(username=username).first()
        if not user:
            user_not_found()
        following_list = Follow.objects.filter(user=user)
        serializer = self.serializer_class(following_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
