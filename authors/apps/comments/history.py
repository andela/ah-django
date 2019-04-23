from .models import Comments


class CommentHistory:
    '''This class is used to get edit history of a particular comment'''

    def get_comment_updates(self, instance):
        '''Gets the edit history of comment if it exists'''
        edits = []
        for edit in list(instance.filter()):
            edit_data = {
                "updated_at": str(edit.history_date),
                "history_id": edit.history_id,
                "body": self.get_body(edit),
            }
            edits.append(edit_data)
        return edits

    def get_body(self, comment):
        '''Get body of the comment'''
        if comment in Comments.comment_history.all():
            return comment.body
