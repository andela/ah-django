from rest_framework import serializers

from authors.apps.profiles.serializers import ProfileSerializer
from authors.apps.profiles.models import Profile


from .models import Bookmarks


class BookmarkSerializer(serializers.ModelSerializer):
    """
    a bookmark serializer
    """
    class Meta:
        model = Bookmarks
        fields = '__all__'
        read_only_fields = ["article", "user"]


class ListBookmarkersSerializer(serializers.ModelSerializer):
    """
        view all bookmarkers
    """
    profile = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Bookmarks
        fields = ["profile", "created_at"]
        read_only_fields = ["article", "user"]

    def get_profile(self, obj):
        profile = Profile.objects.get(user=obj.user)
        return ProfileSerializer(profile,
                                 context={'request':
                                          self.context["request"]}).data
