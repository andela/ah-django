""" This module defines views for profiles """
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Profile
from .renderers import ProfileJsonRenderer
from .serializers import (
    ProfileSerializer, UpdateProfileSerializer)
from rest_framework.generics import (
        UpdateAPIView)


class ProfileListApi(APIView):
    """
    Authenticated user gets all classes
    Get:
    Profiles
    """

    permission_classes = (IsAuthenticated,)
    renderer_classes = (ProfileJsonRenderer,)

    def get(self, request, format=None):
        """
        Return all profiles
        Retrieves all user profiles in the system
        """

        profiles = Profile.objects.all()
        # Return all the details of the users
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class UpdateUserAPIView(UpdateAPIView):
    """
    Gets information of a single user
    """
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ProfileJsonRenderer,)
    serializer_class = UpdateProfileSerializer
    queryset = Profile.objects.all()

    def get_object(self):
        """
        Confirm if the one making the query is
        the owner of the account
        """

        # Only the user logged in can edit their profile
        requester = self.filter_queryset(self.get_queryset())
        requester_user = requester.select_related('user').get(
            user__username=self.request.user.username
        )
        return requester_user

    def patch(self, request, string):
        """
        This method enables the user to edit specific details
        from their profile
        """

        if request.user.username != string:
            return Response((
                {"message": "You don't have permission to edit this profile"}),
                status=status.HTTP_403_FORBIDDEN
            )
        # Get the data from user input
        data = request.data
        # Jsonify the response to a readable view.
        serializer = self.serializer_class(
                        instance=request.user.profile,
                        data=data,
                        partial=True
                    )
        serializer.is_valid()
        serializer.save()
        # Response with the updated data
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class UserProfileView(APIView):
    """
    Display the profile from the route input
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer
    renderer_classes = (ProfileJsonRenderer,)

    def get(self, request, string):
        """
        Return one user profile depending on the
        user defined in te url.
        """

        try:
            # Get the specific user details
            profile_item = Profile.objects.get(user__username=string)

            # If the user is not found, the system should throw
            # an error
        except BaseException:
            return Response(
                {"error": "User profile does not exist."},
                status=status.HTTP_404_NOT_FOUND)

        # Retrieve the user profile in json format
        serializer = ProfileSerializer(
            profile_item,
            context={'request': request})

        # Render the user profile
        return Response(
            {'profile': serializer.data},
            status=status.HTTP_200_OK)
