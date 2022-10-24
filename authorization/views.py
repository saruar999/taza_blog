from core.views import CustomModelViewSet
from core.permissions import DjangoModelPermissions
from .serializers import GroupSerializer, PermissionSerializer


class GroupViewSet(CustomModelViewSet):

    permission_classes = (DjangoModelPermissions,)
    serializer_class = GroupSerializer
    queryset = GroupSerializer.Meta.model.objects.all()


class PermissionViewSet(CustomModelViewSet):

    permission_classes = (DjangoModelPermissions,)
    serializer_class = PermissionSerializer
    queryset = PermissionSerializer.Meta.model.objects.all()
