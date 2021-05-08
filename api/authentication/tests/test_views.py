from django.test import TestCase
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.test import APIRequestFactory

from ..views import RegisterView


class TestRegister(TestCase):
    request_factory = APIRequestFactory()

    def test_should_create_user_when_data_provided(self):
        request = self.request_factory.post('/auth/register/', {'username': 'user', 'password': 'password'})
        response = RegisterView.as_view()(request)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'user')

    def test_should_NOT_allow_duplicate_users(self):
        request = self.request_factory.post('/auth/register/', {'username': 'user', 'password': 'password'})
        request2 = self.request_factory.post('/auth/register/', {'username': 'user', 'password': 'another_pass'})
        response = RegisterView.as_view()(request)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'user')

        response = RegisterView.as_view()(request2)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertListEqual(response.data['username'], ['A user with that username already exists.'])

    def test_should_NOT_allow_missing_username(self):
        request = self.request_factory.post('/auth/register/', {'password': 'password'})
        response = RegisterView.as_view()(request)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertListEqual(response.data['username'], ['This field is required.'])

    def test_should_NOT_allow_empty_username(self):
        request = self.request_factory.post('/auth/register/', {'username': '', 'password': 'password'})
        response = RegisterView.as_view()(request)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertListEqual(response.data['username'], ['This field may not be blank.'])

    def test_should_NOT_allow_empty_password(self):
        request = self.request_factory.post('/auth/register/', {'username': 'user', 'password': ''})
        response = RegisterView.as_view()(request)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertListEqual(response.data['password'], ['This field may not be blank.'])

    def test_should_NOT_allow_missing_password(self):
        request = self.request_factory.post('/auth/register/', {'username': 'user'})
        response = RegisterView.as_view()(request)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertListEqual(response.data['password'], ['This field is required.'])
