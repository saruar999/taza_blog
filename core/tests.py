from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from unittest.mock import MagicMock
from core.models import User, Author
from django.contrib.auth.models import Permission


class CustomApiTestCase(APITestCase):

    model = None
    url = ''
    request_body = {}
    url_kwargs = {}
    headers = {}
    permission_list = []
    test_as_admin = False
    reversed_url = None

    # TEMP USER
    EMAIL = 'temp@test.com'
    PASSWORD = '123'
    FIRST_NAME = 'temp'
    LAST_NAME = 'test'
    GENDER = 'M'

    # SUPERUSER
    SUPER_EMAIL = 'admin@admin.com'
    SUPER_PASSWORD = '123'

    def _test_request(self, method, **kwargs):
        """
            custom function that makes a request to the given url, body and method,
            and then redirects the response to one of the
            testing functions (_test_patch, _test_post, etc...) for testing purposes

            :param method: the api method (post, get, patch, etc...)
            :param headers: headers to be passed with the request
        """
        reversed_url = self.reversed_url if self.reversed_url is not None \
            else reverse(self.url, kwargs=self.url_kwargs)
        test_func_name = '_test_%s' % method
        test_func = getattr(self, test_func_name)
        api_func = getattr(self.client, method)
        if method in ['get', 'delete']:
            res = api_func(reversed_url, **self.headers)
        else:
            res = api_func(reversed_url, self.request_body, **self.headers)

        if res.status_code == 405:
            print(reversed_url)

        test_func(res=res, **kwargs)
        return res

    def _test_delete(self, res, **kwargs):

        expected_status = kwargs.get('expected_status', status.HTTP_204_NO_CONTENT)

        self.assertEqual(res.status_code, expected_status)

    def _test_get(self, res, **kwargs):
        if res.status_code == 400:
            print(res.data)

        expected_status = kwargs.get('expected_status', status.HTTP_200_OK)
        self.assertEqual(res.status_code, expected_status)

    def _test_patch(self, res, **kwargs):

        expected_status = kwargs.get('expected_status', status.HTTP_200_OK)

        # Checking if object was updated
        self.assertEqual(res.status_code, expected_status)

    def _test_post(self, res, **kwargs):

        expected_status = kwargs.get('expected_status', status.HTTP_201_CREATED)

        # Checking if object was created
        self.assertEqual(res.status_code, expected_status)

    def _test_signal(self, signal):

        # Checking if user_created signal was called
        handler = MagicMock()
        signal.connect(handler)

        signal.send(sender=self.model)
        handler.assert_called_once_with(sender=self.model, signal=signal)

    def _test_crud_operation_authorized(self, method):
        self.login_with_permissions()
        self._test_request(method=method)

    def _test_crud_operation_unauthorized(self, method):
        self.logout()
        self._test_request(method=method, expected_status=401)

    def login(self, email, password):
        url = reverse('login')
        body = {
            "email": email,
            "password": password
        }
        res = self.client.post(url, body)
        self.headers.update({'HTTP_AUTHORIZATION': 'Bearer ' + res.data['data']['access']})

    def get_temp_user(self):
        if User.objects.filter(email=self.EMAIL).exists():
            return User.objects.get(email=self.EMAIL)
        else:
            return User.objects.create_verified_user(email=self.EMAIL, password=self.PASSWORD,
                                                     first_name=self.FIRST_NAME, last_name=self.LAST_NAME,
                                                     gender=self.GENDER)

    def get_temp_author(self):
        if User.objects.filter(email=self.EMAIL).exists():
            return Author.objects.get(email=self.EMAIL)
        else:
            return Author.objects.create_verified_user(email=self.EMAIL, password=self.PASSWORD,
                                                     first_name=self.FIRST_NAME, last_name=self.LAST_NAME,
                                                     gender=self.GENDER)

    def login_with_permissions(self, custom_user=None, custom_password=None):

        permissions = Permission.objects.filter(codename__in=self.permission_list)

        user = custom_user if custom_user is not None else self.get_temp_user()

        if self.test_as_admin:
            user.is_staff = True

        [user.user_permissions.add(permission) for permission in permissions]
        user.save()
        self.login(email=user.email,
                   password=custom_password if custom_password is not None else self.PASSWORD)

    def login_superuser(self):
        self.login(email=self.SUPER_EMAIL, password=self.SUPER_PASSWORD)

    def logout(self):
        if self.headers.get('HTTP_AUTHORIZATION'):
            self.headers.pop('HTTP_AUTHORIZATION')


class DetailsTestCaseMixin:
    """
        A Testcase mixin that runs retrieve, update and delete operations when inherited.
        to exclude a test override it in child class and use pass keyword
    """

    def test_retrieve_unauthorized(self):
        self._test_crud_operation_unauthorized(method='get')

    def test_retrieve_authorized(self):
        self._test_crud_operation_authorized(method='get')

    def test_update_unauthorized(self):
        self._test_crud_operation_unauthorized(method='patch')

    def test_update_authorized(self):
        self._test_crud_operation_authorized(method='patch')

    def test_delete_unauthorized(self):
        self._test_crud_operation_unauthorized(method='delete')

    def test_delete_authorized(self):
        self._test_crud_operation_authorized(method='delete')


class ListTestCaseMixin:
    """
           A Testcase mixin that runs list and create operations when inherited.
           to skip a test override it in child class and use pass keyword
    """

    def test_create_unauthorized(self):
        self._test_crud_operation_unauthorized(method='post')

    def test_create_authorized(self):
        self._test_crud_operation_authorized(method='post')

    def test_list_unauthorized(self):
        self._test_crud_operation_unauthorized(method='get')

    def test_list_authorized(self):
        self._test_crud_operation_authorized(method='get')


