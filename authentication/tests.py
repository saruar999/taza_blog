from core.tests import CustomApiTestCase
from core.models.authors import Author
from core.models.admins import Admins
from rest_framework import status


class SelfRegister(CustomApiTestCase):

    url = 'register-author-list'
    request_body = {
            "email": "test@test.com",
            "password": "123",
            "confirm_password": "123",
            "first_name": "test",
            "last_name": "user",
            "gender": "M"
    }

    def setUp(self) -> None:
        self.model = Author

    def test_success(self):

        self._test_request(method='post')

        from django.db.models.signals import post_save
        self._test_signal(signal=post_save)

    def test_unmatching_passwords(self):
        self.request_body.update({'confirm_password': '1234'})

        self._test_request(method='post', expected_status=status.HTTP_400_BAD_REQUEST, expected_count=0)

    def test_duplicate_email(self):

        self._test_request(method='post')

        self._test_request(method='post',
                              expected_status=status.HTTP_400_BAD_REQUEST)


class AccountVerification(CustomApiTestCase):

    model = Author
    url = 'register-author-verify-account'
    request_body = {
        'verification_code': '123456'
    }
    url_kwargs = {}

    user = None

    def setUp(self) -> None:
        self.user = self.model.objects.\
            create_unverified_user(email='test@test.com', password='123', verification_code='123456')

        self.url_kwargs.update({'pk': self.user.id})

    def test_verification(self):

        self._test_request(method='patch')


class RegisterAdmin(CustomApiTestCase):

    model = Admins
    url = 'register-admin-list'

    request_body = {
        "email": "admin@test.com",
        "password": "123",
        "first_name": "test",
        "last_name": "user",
        "gender": "M"
    }

    def tearDown(self) -> None:
        self.logout()

    def test_register_unauthorized(self):
        self._test_request(method='post', expected_status=status.HTTP_401_UNAUTHORIZED)

    def test_register_as_superuser(self):
        self.login_superuser()
        self._test_request(method='post', expected_status=status.HTTP_201_CREATED, expected_count=2)






