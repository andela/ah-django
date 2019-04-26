from rest_framework import serializers

from .models import Follow


class FollowSerializer(serializers.ModelSerializer):
    """This is for following another user"""

    class Meta:
        model = Follow
        fields = ['user', 'followed_user']


class FollowerSerializer(serializers.BaseSerializer):
    """
    Serializer for displaying the name of followed user
    """

    def to_representation(self, obj):
        return {
            'username': obj.followed_user.username,
        }


class FollowerListSerializer(serializers.BaseSerializer):
    """
    Serlializer to display the name of the following user
    """

    def to_representation(self, obj):
        return {
            'username': obj.user.username,
        }
