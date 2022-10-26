from django.contrib.auth.models import Group, Permission, ContentType
from rest_framework import serializers


class GroupSerializer(serializers.ModelSerializer):
    permissions_queryset = Permission.objects.exclude(content_type__app_label__in=['contenttypes', 'sessions'])
    permissions = serializers.SlugRelatedField(many=True,
                                               slug_field='codename',
                                               queryset=permissions_queryset)

    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions']
        extra_kwargs = {
            'id': {
                'read_only': True
            }
        }


class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = ['id', 'codename', 'name']

