from core.tests import CustomApiTestCase
from core.models.authors import Author
from core.models.admins import Admins
from core.models.users import User
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

        super()._test_request(method='post')

        from django.db.models.signals import post_save
        super()._test_signal(signal=post_save)

    def test_unmatching_passwords(self):
        self.request_body.update({'confirm_password': '1234'})

        super()._test_request(method='post', expected_status=status.HTTP_400_BAD_REQUEST, expected_count=0)

    def test_duplicate_email(self):

        super()._test_request(method='post')

        super()._test_request(method='post',
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

        super()._test_request(method='patch', pk=self.user.id,
                              updated_fields={'verification_code': '123456', 'is_verified': True, },)


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
        super().logout()

    def test_register_unauthorized(self):
        super()._test_request(method='post', expected_status=status.HTTP_401_UNAUTHORIZED)

    def test_register_as_superuser(self):
        super().login_superuser()
        super()._test_request(method='post', expected_status=status.HTTP_201_CREATED, expected_count=2)


class LoginUser(CustomApiTestCase):

    url = 'login'
    model = User

    request_body = {
        'email': 'admin@admin.com',
        'password': '123'
    }

    # def test_superuser_login(self):
    #     super()._test_request(method='post', expected_status=status.HTTP_200_OK)
    #




