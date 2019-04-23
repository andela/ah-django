from rest_framework import serializers
from authors import settings
from authors.apps.notifications.middleware import RequestMiddleware

from .models import (Profile, Follow)

User = settings.AUTH_USER_MODEL


class ProfileSerializer(serializers.ModelSerializer):
    """
        This is the default profile serializer
    """
    image = serializers.URLField(required=False)
    bio = serializers.CharField(required=False)
    firstname = serializers.CharField(required=False)
    lastname = serializers.CharField(required=False)
    username = serializers.SerializerMethodField(read_only=True)
    fullname = serializers.SerializerMethodField(read_only=True)
    following = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = ('image',
                  'bio',
                  'id',
                  'username',
                  'firstname',
                  'following',
                  'lastname',
                  'fullname')
        read_only_fields = ('updated_at',)

    def get_username(self, obj):
        """
            return the username of the
            user from the user object
        """
        return obj.user.username

    def get_fullname(self, obj):
        """
        this method returns the concatenated firstname and the lastname
        """
        return obj.firstname + " " + obj.lastname

    def get_following(self, obj):
        """
        get to know if the user requesting to view this profile
        follows the user in question
        """
        request = RequestMiddleware(
            get_response=None).thread_local.current_request
        if request.user.is_authenticated is False:
            return False
        try:
            Follow.objects.get(
                user=request.user,
                following=obj.user)
        except Follow.DoesNotExist:
            return False

        return True


class FollowSerializer(serializers.ModelSerializer):
    firstname = serializers.SerializerMethodField(read_only=True)
    lastname = serializers.SerializerMethodField(read_only=True)
    bio = serializers.SerializerMethodField(read_only=True)
    image = serializers.SerializerMethodField(read_only=True)
    fullname = serializers.SerializerMethodField(read_only=True)
    username = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Follow
        fields = ('image',
                  'bio',
                  'username',
                  'firstname',
                  'lastname',
                  'fullname')

        read_only_fields = ["user", "following"]

    def get_username(self, obj):
        """
            return the username
        """
        return obj.following.username

    def resolveprofilefield(self, obj, field):
        """
            get the properties of a user
        """
        query_set = Profile.objects.get(user=obj.following)
        return ProfileSerializer(query_set).data["{}".format(field)]

    def get_image(self, obj):
        return self.resolveprofilefield(obj, "image")

    def get_bio(self, obj):
        return self.resolveprofilefield(obj, "bio")

    def get_firstname(self, obj):
        return self.resolveprofilefield(obj, "firstname")

    def get_lastname(self, obj):
        return self.resolveprofilefield(obj, "lastname")

    def get_fullname(self, obj):
        return self.resolveprofilefield(obj, "fullname")


class FollowersSerializer(FollowSerializer):
    """
        we are inheriting from the serializer class
        above because this 2 classes have the same structure but
        in this class we need to get the details of the user that is
        doing the following unlike the serializer above where we got
        the details of the user being followed
    """

    def resolveprofilefield(self, obj, field):
        """
            get the properties of a user
        """
        query_set = Profile.objects.get(user=obj.user)
        return ProfileSerializer(query_set).data["{}".format(field)]

    def get_username(self, obj):
        """
            return the username
        """
        return obj.user.username
