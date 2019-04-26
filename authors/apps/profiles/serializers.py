"""
This module defines serialiezers for user profiles
"""
from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """
    Defines serializers for the Profile
    """

    email = serializers.CharField(source='user.email', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    country = serializers.CharField(required=False)
    phone_number = serializers.IntegerField(required=False)
    bio = serializers.CharField(required=False)
    birth_day = serializers.DateField(required=False)
    image = serializers.ImageField(default=None)

    class Meta:
        """
        Meta class to define data for profile serializer
        """

        model = Profile
        fields = (
            'email', 'username', 'first_name', 'last_name', 'country',
            'phone_number', 'bio', 'birth_day', 'image'
        )


class UpdateProfileSerializer(serializers.ModelSerializer):
    """
    This class allows the user to update their own profile
    """

    class Meta:
        """
        Defines the data to be edited
        """

        model = Profile
        fields = (
            'first_name', 'last_name', 'country',
            'phone_number', 'bio', 'birth_day', 'image'
        )

        def update(self, instance, validated_data):
            """
            Allows editing of data
            """
            instance.first_name = validated_data.get(
                'first_name',
                instance.first_name
            )
            instance.last_name = validated_data.get(
                'last_name',
                instance.last_name
            )
            instance.country = validated_data.get(
                'country',
                instance.country
            )
            instance.phone_number = validated_data.get(
                'phone_number',
                instance.phone_number
            )
            instance.bio = validated_data.get(
                'bio',
                instance.bio
            )
            instance.birth_day = validated_data.get(
                'birth_day', instance.birth_day)
            instance.image = validated_data.get(
                'image',
                instance.image
            )
            instance.save()
            return instance
