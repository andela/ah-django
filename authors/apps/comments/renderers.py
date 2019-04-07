from authors.apps.reactions.renderers import ReactionRenderer


class CommentRenderer(ReactionRenderer):
    name = 'comments'


class CommentReplyRenderer(ReactionRenderer):
    name = 'replies'
