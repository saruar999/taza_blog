from core.views import CustomModelViewSet, CustomListMixin
from core.permissions import DjangoModelPermissions
from .serializers import GroupSerializer, PermissionSerializer


class GroupViewSet(CustomModelViewSet):

    permission_classes = (DjangoModelPermissions,)
    serializer_class = GroupSerializer
    queryset = GroupSerializer.Meta.model.objects.all()


class PermissionViewSet(CustomListMixin):

    permission_classes = (DjangoModelPermissions,)
    serializer_class = PermissionSerializer
    queryset = PermissionSerializer.Meta.model.objects.all()
