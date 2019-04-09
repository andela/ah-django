import json

from rest_framework.renderers import JSONRenderer


class NotificationJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        """
        Check for errors key in data
        """

        return json.dumps({
            'notifications': data
        })
