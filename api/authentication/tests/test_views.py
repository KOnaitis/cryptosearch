from django.test import TestCase
from django.urls import reverse
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.test import APIClient


class TestRegister(TestCase):
    client = APIClient()

    def test_should_create_user_when_data_provided(self):
        response = self.client.post(reverse('auth-register'), {'username': 'user', 'password': 'password'})
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'user')

    def test_should_NOT_allow_duplicate_users(self):
        response = self.client.post(reverse('auth-register'), {'username': 'user', 'password': 'password'})
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'user')

        response = self.client.post(reverse('auth-register'), {'username': 'user', 'password': 'another_pass'})
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertListEqual(response.data['username'], ['A user with that username already exists.'])

    def test_should_NOT_allow_missing_username(self):
        response = self.client.post(reverse('auth-register'), {'password': 'password'})
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertListEqual(response.data['username'], ['This field is required.'])

    def test_should_NOT_allow_empty_username(self):
        response = self.client.post(reverse('auth-register'), {'username': '', 'password': 'password'})
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertListEqual(response.data['username'], ['This field may not be blank.'])

    def test_should_NOT_allow_empty_password(self):
        response = self.client.post(reverse('auth-register'), {'username': 'user', 'password': ''})
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertListEqual(response.data['password'], ['This field may not be blank.'])

    def test_should_NOT_allow_missing_password(self):
        response = self.client.post(reverse('auth-register'), {'username': 'user'})
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertListEqual(response.data['password'], ['This field is required.'])
