""" This module renders profiles """

import json

from rest_framework.renderers import JSONRenderer


class ProfileJsonRenderer(JSONRenderer):
    """
    Renders profile in JSON
    """

    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        """
        Perfoms the rendering functionality
        """

        return json.dumps({
            'profiles': data
        })
