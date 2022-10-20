from rest_framework.decorators import action
from .serializers import AuthorSerializer, AdminSerializer, AssignRolesSerializer
from core.views import CustomListMixin, CustomRetrieveMixin, CustomUpdateMixin, CustomCreateMixin
from rest_framework.permissions import DjangoModelPermissions
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import ValidationError


class AuthorViewSet(CustomRetrieveMixin, CustomUpdateMixin, CustomListMixin):

    permission_classes = (DjangoModelPermissions,)
    serializer_class = AuthorSerializer
    queryset = AuthorSerializer.Meta.model.objects.all()


class AdminViewSet(CustomRetrieveMixin, CustomUpdateMixin, CustomListMixin, CustomCreateMixin):

    permission_classes = (DjangoModelPermissions,)
    serializer_class = AdminSerializer
    queryset = AdminSerializer.Meta.model.objects.all()

    @action(methods=['patch'],
            url_path='assign_roles',
            url_name='assign-roles',
            detail=True,
            permission_classes=(DjangoModelPermissions,))
    def assign_roles(self, request, pk=None):

        try:
            admin = self.get_object()
        except Http404:
            return self.return_404()

        serializer = AssignRolesSerializer(admin, data=request.data)

        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        if not isinstance(data, ValidationError):
            res = Response(serializer.data, status=status.HTTP_200_OK)
            return self.get_response(res=res, success=True)
        else:
            return self.return_400()


