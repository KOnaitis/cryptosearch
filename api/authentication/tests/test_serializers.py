from collections import OrderedDict

from django.test import TestCase
from django.contrib.auth import get_user_model
from ..serializers import UserSerializer


class TestRegister(TestCase):
    def test_create_should_create_user(self):
        serializer = UserSerializer()
        user = serializer.create({'username': 'user', 'password': 'pass'})
        self.assertEqual(get_user_model().objects.get(username='user').pk, user.pk)

    def test_create_should_hash_passwords(self):
        serializer = UserSerializer()
        user = serializer.create({'username': 'user', 'password': 'pass'})
        self.assertNotEqual(user.password, 'pass')

    def test_should_only_serialize_username(self):
        serializer = UserSerializer()
        user = serializer.create({'username': 'user', 'password': 'pass'})
        json = serializer.to_representation(user)
        self.assertDictEqual(json, OrderedDict({'username': 'user'}))
