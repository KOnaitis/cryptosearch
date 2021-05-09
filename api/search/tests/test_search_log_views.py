from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_200_OK
from rest_framework.test import APIClient

from api.search.models import AddressSearch, TransactionSearch
from api.search.serializers import AddressSearchSerializer, TransactionSearchSerializer


class TestAddressTransactions(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='log-user', password='pass')
        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def tearDown(self):
        self.user.delete()

    def test_should_list_past_address_searches(self):
        another_user = get_user_model().objects.create(username='address-user', password='pass')
        address = 'bc1q8c0wvzxjfeuzr6xhp7xyxjxjh8r0dsc5ph224'
        expected = []
        for i in range(5):
            log = AddressSearch(address=f'{address}{i}', crypto='btc', page=1, size=10, creator=self.user)
            log.save()
            expected.append(log)
        for i in range(5):
            log = AddressSearch(address=f'{address}{i}', crypto='btc', page=1, size=10, creator=another_user)
            log.save()

        response = self.client.get(reverse('address-transactions-log'))

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertListEqual(response.data, AddressSearchSerializer(many=True).to_representation(expected))
        another_user.delete()

    def test_should_list_past_transaction_searches(self):
        another_user = get_user_model().objects.create(username='transaction-log', password='pass')
        tx = '436b9e8e30592024ce5ea618245fe5eeac3d00cc453af9ca0ecb5611c26f59ef'
        expected = []
        for i in range(5):
            log = TransactionSearch(transaction=f'{tx}{i}', crypto='btc', creator=self.user)
            log.save()
            expected.append(log)
        for i in range(5):
            log = TransactionSearch(transaction=f'{tx}{i}', crypto='btc', creator=another_user)
            log.save()

        response = self.client.get(reverse('transaction-log'))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertListEqual(response.data, TransactionSearchSerializer(many=True).to_representation(expected))
        another_user.delete()
