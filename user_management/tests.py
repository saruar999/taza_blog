from core.tests import ListTestCaseMixin, DetailsTestCaseMixin, CustomApiTestCase
from core.models import Author, Admins
from core.helpers.randoms import generate_random_string


class UserListTestCase(CustomApiTestCase, ListTestCaseMixin):

    url = 'users-list'
    model = Author
    permission_list = ['view_author', 'change_author']

    def test_create_authorized(self):
        pass


class UserDetailTestCase(CustomApiTestCase, DetailsTestCaseMixin):

    url = 'users-detail'
    model = Author
    permission_list = ['view_author', 'change_author']
    request_body = {
        'first_name': generate_random_string(5),
        'last_name': generate_random_string(5),
    }

    def setUp(self) -> None:
        obj = self.model.objects.create_verified_user(email='test@tesst.com',
                                                      password='123',
                                                      first_name='test',
                                                      last_name='testuser',
                                                      gender='M')
        self.url_kwargs = {'pk': obj.id}

    def test_delete_authorized(self):
        pass


class AdminListTestCase(CustomApiTestCase, ListTestCaseMixin):

    permission_list = ['add_admins', 'change_admins', 'view_admins']
    model = Admins
    url = 'admins-list'
    request_body = {
        'email': generate_random_string(5) + '@test.com',
        'password': '123',
        'first_name': generate_random_string(5),
        'last_name': generate_random_string(5),
        'gender': 'M'
    }


class AdminDetailTestCase(CustomApiTestCase, DetailsTestCaseMixin):

    permission_list = ['change_admins', 'view_admins']
    model = Admins
    url = 'admins-detail'
    request_body = {
        'first_name': generate_random_string(5),
        'last_name': generate_random_string(5),
    }

    def setUp(self) -> None:
        obj = self.model.objects.create_admin(email='test@admin.com',
                                              password='123',
                                              first_name='test',
                                              last_name='testuser',
                                              gender='M')
        self.url_kwargs = {'pk': obj.id}

    def test_delete_authorized(self):
        pass


class AdminExtraActionsTestCase(CustomApiTestCase):
    model = Admins
    permission_list = ['change_admins']
    user = None

    def setUp(self) -> None:
        obj = self.model.objects.create_admin(email='test@admin.com',
                                              password='123',
                                              first_name='test',
                                              last_name='testuser',
                                              gender='M')
        self.url_kwargs = {'pk': obj.id}
        self.user = obj

    def test_change_password(self):
        self.request_body = {
            'password': '123',
            'new_password': '456',
            'confirm_new_password': '456'
        }
        self.url = 'admins-change-password'

        self.login_with_permissions(custom_user=self.user)
        self._test_request(method='patch')
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(self.request_body['new_password']))

    def test_assign_roles_to_admin(self):
        self.request_body = {
            'roles': ['moderator']
        }
        self.url = 'admins-assign-roles'

        self.login_with_permissions()
        self._test_request(method='patch')
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_staff)

    def test_remove_roles_from_admin(self):
        self.request_body = {
            'roles': ['moderator']
        }
        self.url = 'admins-remove-roles'

        self.login_with_permissions()
        self._test_request(method='patch')
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_staff)


class AuthorExtraActionsTestCase(CustomApiTestCase):
    model = Author
    permission_list = ['change_author']
    user = None

    def setUp(self) -> None:
        obj = self.model.objects.create_admin(email='test@admin.com',
                                              password='123',
                                              first_name='test',
                                              last_name='testuser',
                                              gender='M')
        self.url_kwargs = {'pk': obj.id}
        self.user = obj

    def test_change_password(self):
        self.request_body = {
            'password': '123',
            'new_password': '456',
            'confirm_new_password': '456'
        }
        self.url = 'users-change-password'

        self.login_with_permissions(custom_user=self.user)
        self._test_request(method='patch')
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(self.request_body['new_password']))



#   TODO: try this
#   @classmethod
#   def x(cls):
#     setattr(cls, test_function, _test_function)