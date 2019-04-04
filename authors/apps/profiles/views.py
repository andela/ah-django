from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter


from .serializers import (ProfileSerializer)
from .models import Profile


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
                                  self.serializer_class(profile).data},
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
                instance=profile, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'profile': serializer.data}, status.HTTP_200_OK)
        except Profile.DoesNotExist:
            Response(data={"error": "Profile not found"},
                     status=status.HTTP_404_NOT_FOUND)
