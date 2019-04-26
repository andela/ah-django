""" This module defines serializers for notifications """
from notifications.models import Notification
from rest_framework import serializers


class NotififcaionSerializers(serializers.ModelSerializer):
    """ Class defines serializers for notifications """

    class Meta:
        """ Defines fields to be returned to user """
        model = Notification

        fields = ('id', 'timestamp', 'unread', 'description')
