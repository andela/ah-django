""" This module defines the highlighter serializers """
from rest_framework import serializers
from .models import Highlight


class HighlightSerializer(serializers.ModelSerializer):
    """ This class defines a highlight datafields """
    comment = serializers.CharField(required=False)

    class Meta:

        model = Highlight
        fields = ("highlighter", "article_id", "highlight", "comment")
