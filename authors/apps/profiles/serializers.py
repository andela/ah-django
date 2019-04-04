from rest_framework import serializers
from authors import settings


from .models import Profile

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

    class Meta:
        model = Profile
        fields = ('image',
                  'bio',
                  'id',
                  'username',
                  'firstname',
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
