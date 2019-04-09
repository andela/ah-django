from rest_framework import generics, status
from rest_framework.response import (Response)
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db import IntegrityError

from rest_framework.permissions import (IsAuthenticated,
                                        AllowAny)

from .serializers import (
    ProfileSerializer, FollowSerializer, FollowersSerializer)
from .models import (Profile, Follow)
from authors.apps.authentication.models import User


class ViewAllProfiles(generics.ListAPIView):
    """
        this view will enable you to view all profiles in
        the profiles table.
    """
    serializer_class = ProfileSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('bio', 'user__email', 'user__username')
    ordering_fields = ('bio', 'user__username')
    queryset = Profile.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        """
            pass the view context to the serializer
        """
        return {"request": self.request}


class ProfileView(generics.RetrieveUpdateAPIView):
    '''
    class view to update or get a user profile
    '''
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    lookup_field = "username"

    def get(self, request, username, *args, **kwargs):
        """Retrieve a single profile"""
        try:

            profile = Profile.objects.get(
                user__username__iexact=username)
            return Response(data={"profile":
                                  self.serializer_class(
                                      profile,
                                      context={'request': request}).data},
                            status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response(data={"error": "Profile not found"},
                            status=status.HTTP_404_NOT_FOUND)

    def put(self, request, username, *args, **kwargs):
        """update a single profile"""
        # update the profile with the fields provided
        try:
            profile = Profile.objects.get(
                user__username__iexact=username)
            # check if the username in the profile
            # matches the username of the requester
            if profile.user.username != request.user.username:
                data = {'error':
                        'You are not allowed to edit or delete this profile'}
                return Response(data, status.HTTP_403_FORBIDDEN)
            serializer = self.serializer_class(
                instance=profile,
                data=request.data,
                partial=True, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'profile': serializer.data}, status.HTTP_200_OK)
        except Profile.DoesNotExist:
            Response(data={"error": "Profile not found"},
                     status=status.HTTP_404_NOT_FOUND)


class FollowersView(generics.RetrieveAPIView):
    '''
        class to view user followers
    '''
    permission_classes = (AllowAny,)
    serializer_class = FollowersSerializer
    queryset = Follow.objects.all()
    lookup_field = "username"

    def get(self, request, username, *args, **kwargs):
        """Retrieve a single profile"""
        try:

            Profile.objects.get(
                user__username__iexact=username)

        except Profile.DoesNotExist:
            return Response(data={
                "error":
                "A User with the username {} is not found".format(username)},
                status=status.HTTP_404_NOT_FOUND)
        userfollowers = Follow.objects.filter(
            following__username__iexact=username
        )
        return Response(data={"followers":
                              self.serializer_class(userfollowers,
                                                    many=True).data},
                        status=status.HTTP_200_OK)


class FollowingView(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()
    lookup_field = "username"

    def get(self, request, username, *args, **kwargs):
        """Retrieve a single profile"""
        try:

            Profile.objects.get(
                user__username__iexact=username)

        except Profile.DoesNotExist:
            return Response(data={
                "error":
                "A User with the username {} is not found".format(username)},
                status=status.HTTP_404_NOT_FOUND)
        userfollowers = Follow.objects.filter(
            user__username__iexact=username
        )
        return Response(data={"following":
                              self.serializer_class(userfollowers,
                                                    many=True).data},
                        status=status.HTTP_200_OK)


class FollowView(generics.CreateAPIView, generics.DestroyAPIView):
    """
        class to view follow a specific user.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()
    lookup_field = "username"

    def post(self, request, username, *args, **kwargs):
        try:

            user = User.objects.get(
                username__iexact=username)

        except User.DoesNotExist:
            return Response(data={
                "error":
                "A User with the username {} is not found".format(username)},
                status=status.HTTP_404_NOT_FOUND)

        data = {
        }

        serializer = self.serializer_class(
            data=data
        )
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save(following=user, user=self.request.user)
        except IntegrityError:
            return Response(data={
                "error": "You follow {} already".format(username)
            }, status=status.HTTP_409_CONFLICT)
        return Response(data={
            "following": serializer.data
        }, status=status.HTTP_201_CREATED)

    def delete(self, request, username, *args, **kwargs):

        try:

            User.objects.get(
                username__iexact=username)

        except User.DoesNotExist:
            return Response(data={
                "error":
                "A User with the username {} was not found".format(username)},
                status=status.HTTP_404_NOT_FOUND)
        try:
            follow = Follow.objects.get(
                following__username__iexact=username,
                user=self.request.user)
            follow.delete()
            return Response(data={
                "data":
                    "You have successfully unfollowed {}".format(username)
            })
        except Follow.DoesNotExist:
            return Response(data={
                "error":
                "You had not followed {} so cannot unfollow".format(username)
            }, status=status.HTTP_404_NOT_FOUND)
