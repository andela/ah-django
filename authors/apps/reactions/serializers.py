from rest_framework import serializers

from .models import UserReaction


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserReaction
        fields = '__all__'
