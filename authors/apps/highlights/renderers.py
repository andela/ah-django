""" Define data presentation to the user """
import json

from rest_framework.renderers import JSONRenderer


class RenderHighlights(JSONRenderer):
    """ Defines the rendering """
    charset = 'utf-8'

    def render(self, data, media_type=None, render_context=None):
        """ This method defins the way data is rendered """

        return json.dumps({
            'highlights': data
        })
