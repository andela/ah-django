import json

from rest_framework.renderers import JSONRenderer


class ArticleRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, render_context=None):
        return json.dumps({
            'articles': data
        })
