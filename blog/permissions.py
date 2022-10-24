from rest_framework.permissions import BasePermission


class CanUpdateDeletePost(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method == 'PATCH' or request.method == 'DELETE':
            return obj.post_author == request.user or request.user.is_moderator or request.user.is_superuser
        else:
            return True
