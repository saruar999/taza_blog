from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group
from django.db.models import Manager
from ..helpers.email import custom_send_mail


class CustomUserManager(BaseUserManager):

    """
        Overriding default manager functions to remove username field,
        and make email the user's unique identifier.

        It also adds create_unverified_user function which set the user's is_verified to false.
    """

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    def create_unverified_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_verified', False)
        return self._create_user(email, password, **extra_fields)


class VerifiedUsers(Manager):
    """
        Custom manager that overrides the default manager's queryset,
        to create a queryset of only verified users.
    """

    def get_queryset(self):
        return super().get_queryset().filter(is_verified=True)


class User(AbstractBaseUser, PermissionsMixin):

    models = models

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name', 'gender']

    GENDER_MALE = 'M'
    GENDER_FEMALE = 'F'
    GENDER_OTHER = 'O'

    GENDER_CHOICES = [
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    ]

    first_name = models.CharField(max_length=50, help_text="User's first name")

    last_name = models.CharField(max_length=50, help_text="User's last name")

    gender = models.CharField(choices=GENDER_CHOICES, max_length=1, help_text="User's Gender")

    email = models.EmailField(max_length=255, unique=True, help_text="User's unique email address")

    is_staff = models.BooleanField(
        default=False,
        help_text="Indicates whether this user is admin",
    )

    is_active = models.BooleanField(
        default=True,
        help_text="Indicates whether this user is active",
    )

    is_verified = models.BooleanField(default=False, help_text="Indicator for email verification")

    verification_code = models.CharField(blank=True, null=True, max_length=10)

    objects = CustomUserManager()
    verified_users = VerifiedUsers()

    class Meta:
        abstract = False

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def send_verification_email(self):

        message = 'verification code for user: %s\n\nyour verification code is: \n%s' % (self.id, self.verification_code)
        subject = 'Verification Code'
        recipient_list = [self.email]

        custom_send_mail(message=message, subject=subject,
                         recipient_list=recipient_list, fail_silently=True)
        pass

    def assign_group(self, name):
        _group = Group.objects.get(name=name)
        if not self.groups.filter(name=_group.name).exists():
            self.groups.add(_group)

