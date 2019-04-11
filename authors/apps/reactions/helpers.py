"""
    This module contains shared functions
    that are regularly called in making object reactions
"""
from .models import UserReaction

from django.contrib.contenttypes.models import ContentType
from rest_framework import status


class DisLikeReaction:
    """
        Handles like and dislike reactions
    """

    def mofidy_reaction(self, instance, user, inherited_react, name='article'):
        """
            Interacts with the model on a reaction request
            by updating the `reactions` field of an object
            to fit the posted request.

            Parameters:
            -------------
            instance: instance
                Content-type object
            user: instance
                User sending the request
            inherited_react: int
                The UserReacitonView class `reaction` attribute
            name: str, optional, default='article'
                The name of the key field in the describing the queried
                object
        """

        self.reaction = inherited_react

        try:
            like_status = UserReaction.objects.get(
                content_type=ContentType.objects.get_for_model(
                    instance),
                object_id=instance.id,
                user=user
            )
            status_ = status.HTTP_200_OK

            if like_status.user_reaction is not self.reaction:
                like_status.user_reaction = self.reaction
                like_status.save(update_fields=['user_reaction'])
                msg = 'Reaction changed'
            else:
                like_status.delete()
                msg = 'Reaction Removed'
        except UserReaction.DoesNotExist:
            instance.user_reaction.create(
                user_reaction=self.reaction,
                user=user)
            msg = "Reaction Created"
            status_ = status.HTTP_201_CREATED

        response = {'message': msg}
        data = {
            name: instance.slug if hasattr(instance, 'slug')
            else instance.body,
            'likes': instance.
            user_reaction.likes.count(),
            'dislikes': instance.
            user_reaction.dislikes.count(),
            'participated_users': instance.
            user_reaction.fetch_popularity_status()
        }
        response['data'] = data

        return response, status_


dislikeReaction = DisLikeReaction()
