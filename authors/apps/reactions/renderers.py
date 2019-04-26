import json

from rest_framework import renderers


class ReactionRenderer(renderers.JSONRenderer):
    name = 'reaction'
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):

        try:
            errors = data.get('detail', None)

            if errors:
                # As mentioned about, we will let the default
                # JSONRenderer handle
                # rendering errors.
                return super(ReactionRenderer, self).render({'errors': data})
        except AttributeError:
            return json.dumps({self.name: data})
        return json.dumps(
            {self.name: data}
        )
