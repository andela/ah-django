from rest_framework import serializers

from authors.apps.profiles.serializers import ProfileSerializer
from authors.apps.profiles.models import Profile
from .models import ReadStats

# User = settings.AUTH_USER_MODEL


class UserStatsSerializer(serializers.ModelSerializer):
    """
        This is the serializer for a specific user
    """
    article = serializers.SerializerMethodField()

    class Meta:
        model = ReadStats
        fields = ('views', 'article',)
        read_only_fields = ('article',)

    def get_article(self, obj):
        return {
            "title": obj.article.title,
            "slug": obj.article.slug,
        }


class ArticleStatsSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = ReadStats
        fields = ('views', 'user',)
        read_only_fields = ('user',)

    def get_user(self, obj):
        profile = Profile.objects.get(user=obj.user)
        return ProfileSerializer(profile).data


class AdminStatsSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    article = serializers.SerializerMethodField()

    class Meta:
        model = ReadStats
        fields = ('views', 'user', 'article',)
        read_only_fields = ('user', 'article')

    def get_user(self, obj):
        profile = Profile.objects.get(user=obj.user)
        return ProfileSerializer(profile).data

    def get_article(self, obj):
        return {
            "title": obj.article.title,
            "slug": obj.article.slug,
        }
