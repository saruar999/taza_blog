from .users import User, CustomUserManager


class CustomAdminManager(CustomUserManager):

    def create_user(self, email, password, **extra_fields):
        return self.create_superuser(email, password, **extra_fields)


class Admins(User):

    objects = CustomAdminManager()

    def assign_superuser_group(self):
        self.assign_group(name='superuser')


