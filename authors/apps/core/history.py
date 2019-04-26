"""
    This module holds a helper class for
    retireving of model history records
"""
from django.db.models import Q

from authors.apps.comments.models import Comment


class ModelHistory:
    """
        Makes record responses to requests
        of item histories
    """

    def get_update_records(self, instance):
        """
            Retrieves the editing history of
            a comment custom in JSON form
        """
        records = []

        update = '~'
        create = '+'
        for record in list(instance.filter(
                Q(history_type=create) | Q(history_type=update))):
            history_data = {
                "body": self.retreive_body(record),
                "alter_date": str(record.history_date),
                "change_type": self.get_worded_history(record.history_type),
                "history_id": record.history_id
            }
            records.append(history_data)
        return records

    def retreive_body(self, rec):
        """
            Returns the body field of a comment
            item
        """
        return rec.body if rec in Comment.comment_history.all() \
            else rec.reply_to

    def get_worded_history(self, symbol):
        """
            Returns a word definition of the
            history change type from the history symbol
        """
        return 'edited' if symbol == '~' else 'created'
