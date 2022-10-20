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
    model_choices = ContentType.objects\
        .exclude(app_label__in=['contenttypes', 'sessions']).values_list('model', flat=True)

    model = serializers.ChoiceField(choices=model_choices, write_only=True)

    class Meta:
        model = Permission
        fields = ['id', 'codename', 'name', 'model']
        extra_kwargs = {
            'id': {
                'read_only': True
            }
        }

    def create(self, validated_data):
        model = validated_data.pop('model')

        content_type = ContentType.objects.get(model=model)

        return Permission.objects.create(**validated_data, content_type=content_type)
