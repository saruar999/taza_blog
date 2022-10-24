from rest_framework.permissions import BasePermission, DjangoModelPermissions as RestModelPermissions


class DjangoModelPermissions(RestModelPermissions):

    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }


class IsSuperuser(BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.is_superuser:
            return request.user.is_superuser
        else:
            return True


class IsNotUser(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.id != request.user.id or request.user.is_superuser


class IsUser(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id or request.user.is_superuser
