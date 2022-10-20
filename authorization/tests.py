from core.tests import ListTestCaseMixin, DetailsTestCaseMixin, CustomApiTestCase
from django.contrib.auth.models import Group, Permission, ContentType
from core.helpers.randoms import generate_random_string


class RoleBaseTestCase:

    def __init__(self, method_name):
        permissions = Permission.objects.all().values_list('codename', flat=True)[:5]

        self.request_body = {
            'name': generate_random_string(length=10),
            'permissions': list(permissions)
        }
        super().__init__(method_name)


class RoleListTestCase(RoleBaseTestCase, CustomApiTestCase, ListTestCaseMixin):

    url = 'roles-list'
    model = Group
    permission_list = ['view_group', 'add_group']


class RoleDetailTestCase(RoleBaseTestCase, CustomApiTestCase, DetailsTestCaseMixin):

    url = 'roles-detail'
    model = Group
    permission_list = ['view_group', 'change_group', 'delete_group']

    def setUp(self) -> None:
        obj = self.model.objects.create(name=generate_random_string(5))
        permissions = Permission.objects.first()
        obj.permissions.add(permissions)
        self.url_kwargs = {'pk': obj.id}


class PermissionBaseTestCase:

    def __init__(self, method_name):
        model = ContentType.objects.all().values_list('model', flat=True).last()
        self.request_body = {
            'name': generate_random_string(length=10),
            'model': model,
            'codename': generate_random_string(length=10)
        }
        super().__init__(method_name)


class PermissionListTestCase(PermissionBaseTestCase, CustomApiTestCase, ListTestCaseMixin):

    url = 'permissions-list'
    model = Permission
    permission_list = ['view_permission', 'add_permission']


class PermissionDetailTestCase(PermissionBaseTestCase, CustomApiTestCase, DetailsTestCaseMixin):

    url = 'permissions-detail'
    model = Permission
    permission_list = ['view_permission', 'change_permission', 'delete_permission']

    def setUp(self) -> None:
        content_type = ContentType.objects.all().last()
        obj = self.model.objects.create(name=generate_random_string(5),
                                        codename=generate_random_string(5),
                                        content_type=content_type)
        self.url_kwargs = {'pk': obj.id}
