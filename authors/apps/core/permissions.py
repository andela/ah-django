"""
    This module contains customized permission classes
"""

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
     Object-level permission to only allow owners of a resource to
     perform write actions on the resource.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user
