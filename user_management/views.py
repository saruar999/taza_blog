from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser

from core.permissions import IsSuperuser, IsNotUser, IsUser, DjangoModelPermissions
from core.views import CustomListMixin, CustomRetrieveMixin, CustomUpdateMixin, CustomCreateMixin

from .serializers import AuthorSerializer, AdminSerializer, AssignRolesSerializer, \
    RemoveRolesSerializer, ChangePasswordSerializer, ProfileSerializer


class ChangePasswordMixin:

    change_password_model = AuthorSerializer.Meta.model
    @action(methods=['patch'], url_name='change-password', url_path='change_password', detail=False,
            permission_classes=(DjangoModelPermissions, IsUser))
    def change_password(self, request, pk=None):
        user = request.user
        classified_user = self.change_password_model.return_classified_user_from_request_user(user)
        serializer = ChangePasswordSerializer(classified_user, data=request.data)
        return self.serialize_extra_action(serializer=serializer, message='password changed')


class AuthorViewSet(CustomRetrieveMixin, CustomUpdateMixin, CustomListMixin, ChangePasswordMixin):

    permission_classes = (DjangoModelPermissions, IsAdminUser)
    serializer_class = AuthorSerializer
    queryset = AuthorSerializer.Meta.model.objects.all()

    user_lookup_kwarg = 'id'

    @action(methods=['get', 'patch'], url_name='user-profile', url_path='user_profile', detail=False,
            permission_classes=(DjangoModelPermissions, IsUser,))
    def user_profile(self, request):
        user = request.user
        author = AuthorSerializer.Meta.model.return_classified_user_from_request_user(user)
        if request.method == 'PATCH':
            serializer = ProfileSerializer(author, data=request.data)
            return self.serialize_extra_action(serializer=serializer)
        else:
            serializer = ProfileSerializer(author)
            return self.return_extra_action(serializer)


class AdminViewSet(CustomRetrieveMixin, CustomUpdateMixin, CustomListMixin, CustomCreateMixin, ChangePasswordMixin):

    permission_classes = (DjangoModelPermissions, IsSuperuser)
    serializer_class = AdminSerializer
    queryset = AdminSerializer.Meta.model.objects.all()
    change_password_model = AdminSerializer.Meta.model
    @action(methods=['patch'],
            url_path='assign_roles',
            url_name='assign-roles',
            detail=True,
            permission_classes=(DjangoModelPermissions, IsSuperuser, IsNotUser))
    def assign_roles(self, request, pk=None):
        admin = self.get_object()
        if self.error_res is not None:
            return self.error_res
        serializer = AssignRolesSerializer(admin, data=request.data)

        return self.serialize_extra_action(serializer=serializer, message='roles assigned')

    @action(methods=['patch'],
            url_path='remove_roles',
            url_name='remove-roles',
            detail=True,
            permission_classes=(DjangoModelPermissions, IsSuperuser, IsNotUser))
    def remove_roles(self, request, pk=None):

        admin = self.get_object()
        if self.error_res is not None:
            return self.error_res
        serializer = RemoveRolesSerializer(admin, data=request.data)

        return self.serialize_extra_action(serializer=serializer, message='roles removed')

