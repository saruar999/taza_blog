from core.models import Author, Admins
from rest_framework import serializers
from django.contrib.auth.models import Group
from rest_framework.serializers import ValidationError


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ['id', 'email', 'first_name', 'last_name', 'gender']
        extra_kwargs = {
            'id': {
                'read_only': True,
            },
            'email': {
                'read_only': True,
            },
        }


class AdminSerializer(serializers.ModelSerializer):

    roles = serializers.SlugRelatedField(read_only=True, many=True, slug_field='name', source='groups')

    class Meta:
        model = Admins
        fields = ['id', 'email', 'first_name', 'last_name', 'gender', 'roles']
        extra_kwargs = {
            'id': {
                'read_only': True,
            },
            'email': {
                'read_only': True,
            },
        }


class AssignRolesSerializer(serializers.Serializer):
    roles = serializers.ListSerializer(child=serializers.CharField(), min_length=1, write_only=True)

    def update(self, instance, validated_data):
        roles = validated_data.get('roles')
        for role in roles:
            try:
                group = Group.objects.get(name__iexact=role)
                instance.groups.add(group)
            except Group.DoesNotExist:
                return ValidationError({'error': 'role does not exist'})

        instance.save()
        return instance

    def create(self, validated_data):
        pass
