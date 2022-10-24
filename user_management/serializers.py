from core.models import Author, Admins, User
from rest_framework import serializers
from django.contrib.auth.models import Group
from rest_framework.serializers import ValidationError
from blog.serializers import PostsSerializer


class ChangePasswordSerializer(serializers.Serializer):

    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    new_password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    confirm_new_password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        password = validated_data['password']
        new_password = validated_data['new_password']
        confirm_new_password = validated_data['confirm_new_password']
        if instance.check_password(password):
            if new_password == confirm_new_password:
                instance.set_password(new_password)
                instance.save()
                return instance
            else:
                return ValidationError('passwords do not match')

        else:
            return ValidationError('password is wrong')




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
                if instance.groups.count() == 0:
                    instance.is_staff = True
                group = Group.objects.get(name__iexact=role)
                instance.groups.add(group)
            except Group.DoesNotExist:
                return ValidationError('role does not exist')

        instance.save()
        return instance

    def create(self, validated_data):
        pass


class RemoveRolesSerializer(AssignRolesSerializer):

    def update(self, instance, validated_data):
        roles = validated_data.get('roles')

        for role in roles:
            try:
                group = Group.objects.get(name__iexact=role)
                instance.groups.remove(group)
                if instance.groups.count() == 0:
                    instance.is_staff = False

            except Group.DoesNotExist:
                return ValidationError('role does not exist')

        instance.save()
        return instance


class ProfileSerializer(serializers.ModelSerializer):

    favorite_posts = PostsSerializer(read_only=True, many=True)
    liked_posts = PostsSerializer(read_only=True, many=True)

    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'gender', 'email', 'favorite_posts', 'liked_posts']
        extra_kwargs = {
            'email': {
                'read_only': True,
            },
        }
