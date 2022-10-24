from rest_framework.serializers import ModelSerializer, \
    CharField, \
    ValidationError, \
    Serializer, \
    ListSerializer
from core.models.authors import Author
from core.models.admins import Admins
from core.models.users import User
from core.helpers.randoms import generate_verification_code
from django.contrib.auth.models import Group


class BaseRegisterSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'gender']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            },
            'id': {
                'read_only': True
            }
        }

    def get_model(self):
        return self.Meta.model

    def validate(self, attrs):
        email = attrs['email']

        if Author.objects.filter(email=email).exists():
            return ValidationError('user with this email already exists')

        return attrs

    def _create(self, validated_data, **extra_fields):

        email = validated_data['email']
        first_name = validated_data['first_name']
        last_name = validated_data['first_name']
        gender = validated_data['gender']
        password = validated_data['password']

        model = self.get_model()

        instance = model.objects.create_user(email=email, password=password,
                                             first_name=first_name, last_name=last_name,
                                             gender=gender, **extra_fields)

        return instance


class RegisterSerializer(BaseRegisterSerializer):

    confirm_password = CharField(write_only=True, style={'input_type': 'password'})

    class Meta(BaseRegisterSerializer.Meta):
        model = Author
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'gender', 'confirm_password']

    def validate(self, attrs):
        super().validate(attrs)

        password = attrs['password']
        confirm_password = attrs['confirm_password']

        if confirm_password != password:
            raise ValidationError({'password': 'passwords do not match'})

        return attrs

    def create(self, validated_data):
        verification_code = generate_verification_code(length=6)
        return self._create(validated_data, verification_code=verification_code)


class AdminRegisterSerializer(BaseRegisterSerializer):
    roles = ListSerializer(child=CharField(), min_length=1, write_only=True)

    class Meta(BaseRegisterSerializer.Meta):
        model = Admins
        fields = ['email', 'password', 'first_name', 'last_name', 'gender', 'roles']

    def create(self, validated_data):
        roles = validated_data.pop('roles')

        instance = self._create(validated_data)

        for role in roles:
            try:
                group = Group.objects.get(name__iexact=role)
                instance.groups.add(group)
            except Group.DoesNotExist:
                return ValidationError('role does not exist')

        instance.save()
        return instance


class VerifyEmailSerializer(Serializer):

    verification_code = CharField(max_length=6, write_only=True)

    def verify_user(self, instance):
        instance.is_verified = True

        from core.apps import user_verified
        user_verified.send(sender=self.__class__, instance=instance)

        instance.save()
        return instance

    def update(self, instance, validated_data):
        if instance.is_verified:
            return ValidationError('User already verified')
        code = validated_data.get('verification_code')
        if instance.verification_code == code:
            return self.verify_user(instance)
        else:
            return ValidationError('incorrect verification code')

    def create(self, validated_data):
        pass








