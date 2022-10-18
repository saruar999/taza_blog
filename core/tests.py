from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from unittest.mock import MagicMock


class CustomApiTestCase(APITestCase):

    model = None
    url = ''
    request_body = {}
    url_kwargs = {}
    headers = {}

    def _test_request(self, method, **kwargs):
        """
            custom function that makes a request to the given url, body and method,
            and then redirects the response to one of the
            testing functions (_test_patch, _test_post, etc...) for testing purposes

            :param method: the api method (post, get, patch, etc...)
            :param headers: headers to be passed with the request
        """

        reversed_url = reverse(self.url, kwargs=self.url_kwargs)

        test_func_name = '_test_%s' % method
        test_func = getattr(self, test_func_name)
        api_func = getattr(self.client, method)
        res = api_func(reversed_url, self.request_body, **self.headers)
        test_func(res=res, **kwargs)
        return res

    def _test_patch(self, res, **kwargs):

        expected_status = kwargs.get('expected_status', status.HTTP_200_OK)
        pk = kwargs.get('pk', None)
        updated_fields = kwargs.get('updated_fields', {})

        # Checking if object was updated
        self.assertEqual(res.status_code, expected_status)

        # Checking updated values
        if pk is not None:
            obj = self.model.objects.get(pk=pk)
            for key, value in updated_fields.items():
                self.assertEqual(getattr(obj, key), value)

    def _test_post(self, res, **kwargs):

        expected_status = kwargs.get('expected_status', status.HTTP_201_CREATED)
        expected_count = kwargs.get('expected_count', 1)

        print(self.model.objects.all())
        # Checking if object was created
        self.assertEqual(res.status_code, expected_status)
        self.assertEqual(self.model.objects.count(), expected_count)

    def _test_signal(self, signal):

        # Checking if user_created signal was called
        handler = MagicMock()
        signal.connect(handler)

        signal.send(sender=self.model)
        handler.assert_called_once_with(sender=self.model, signal=signal)

    def login_superuser(self):
        url = reverse('login')
        body = {
            "email": "admin@admin.com",
            "password": "123"
        }
        res = self.client.post(url, body)
        self.headers.update({'HTTP_AUTHORIZATION': 'Bearer ' + res.data['data']['access']})

    def logout(self):
        if self.headers.get('HTTP_AUTHORIZATION'):
            self.headers.pop('HTTP_AUTHORIZATION')


