from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.test import APIClient

from api.search.models import AddressSearch, TransactionSearch


class TestAddressTransactions(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='blockchain-client', password='pass')
        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def tearDown(self):
        self.user.delete()

    @patch('api.search.blockchain_client.client.BlockchainClient.transaction')
    def test_transaction_detail_should_allow_btc(self, mock):
        tx = '436b9e8e30592024ce5ea618245fe5eeac3d00cc453af9ca0ecb5611c26f59ef'
        url = reverse('transaction-detail', kwargs={'crypto': 'btc', 'tx': tx})
        mock.return_value = []
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_200_OK)
        mock.assert_called_once_with(crypto='btc', tx=tx)

    @patch('api.search.blockchain_client.client.BlockchainClient.transactions_for_address')
    def test_address_search_should_allow_btc(self, mock):
        url = reverse('address-transactions',
                      kwargs={'crypto': 'btc', 'address': 'bc1q8c0wvzxjfeuzr6xhp7xyxjxjh8r0dsc5ph224d'})
        mock.return_value = {'transactions': []}
        response = self.client.get(url, {'page': 0})
        self.assertEqual(response.status_code, HTTP_200_OK)
        mock.assert_called_once_with(
            crypto='btc',
            address='bc1q8c0wvzxjfeuzr6xhp7xyxjxjh8r0dsc5ph224d',
            page=0,
            size=50)

    @patch('api.search.blockchain_client.client.BlockchainClient.transaction')
    def test_transaction_detail_should_allow_eth(self, mock):
        tx = '0x8d3eb0836e0c73ee60c3d89d06d830f8c31c19f47c1dc6fbfc9e02e20852352b'
        url = reverse('transaction-detail', kwargs={'crypto': 'eth', 'tx': tx})
        mock.return_value = []
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_200_OK)
        mock.assert_called_once_with(crypto='eth', tx=tx)

    @patch('api.search.blockchain_client.client.BlockchainClient.transactions_for_address')
    def test_address_search_should_allow_eth(self, mock):
        url = reverse('address-transactions',
                      kwargs={'crypto': 'eth', 'address': '0xaa62dc6cd0123d5bb1e080e61f5fe508b7c8744e'})
        mock.return_value = {'transactions': []}
        response = self.client.get(url, {'page': 1})
        self.assertEqual(response.status_code, HTTP_200_OK)
        mock.assert_called_once_with(
            crypto='eth',
            address='0xaa62dc6cd0123d5bb1e080e61f5fe508b7c8744e',
            page=1,
            size=50)

    @patch('api.search.blockchain_client.client.BlockchainClient.transaction')
    def test_transaction_detail_should_allow_bch(self, mock):
        tx = '5aaa2ecc901a6d42fa27eb7ca1535df76ffc75416dd54180c4f9034b9c6d4dc5'
        url = reverse('transaction-detail', kwargs={'crypto': 'bch', 'tx': tx})
        mock.return_value = []
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_200_OK)
        mock.assert_called_once_with(crypto='bch', tx=tx)

    @patch('api.search.blockchain_client.client.BlockchainClient.transactions_for_address')
    def test_address_search_should_allow_bch(self, mock):
        url = reverse('address-transactions',
                      kwargs={'crypto': 'bch', 'address': 'qqtgm0njzgctkmhc28q6530zvjs0pjedxq4d4r7qfr'})
        mock.return_value = {'transactions': []}
        response = self.client.get(url, {'page': 2})
        self.assertEqual(response.status_code, HTTP_200_OK)
        mock.assert_called_once_with(
            crypto='bch',
            address='qqtgm0njzgctkmhc28q6530zvjs0pjedxq4d4r7qfr',
            page=2,
            size=50)

    @patch('api.search.blockchain_client.client.BlockchainClient.transactions_for_address')
    def test_address_search_should_set_page_to_0_by_default(self, mock):
        url = reverse('address-transactions',
                      kwargs={'crypto': 'bch', 'address': 'qqtgm0njzgctkmhc28q6530zvjs0pjedxq4d4r7qfr'})
        mock.return_value = {'transactions': []}
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_200_OK)
        mock.assert_called_once_with(
            crypto='bch',
            address='qqtgm0njzgctkmhc28q6530zvjs0pjedxq4d4r7qfr',
            page=0,
            size=50)

    @patch('api.search.blockchain_client.client.BlockchainClient.transactions_for_address')
    def test_should_create_address_search_log(self, mock):
        url = reverse('address-transactions',
                      kwargs={'crypto': 'bch', 'address': 'searchlog'})
        mock.return_value = {'transactions': []}
        self.assertFalse(AddressSearch.objects.filter(crypto='bch', address='searchlog', creator=self.user).exists())
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertTrue(AddressSearch.objects.filter(crypto='bch', address='searchlog', creator=self.user).exists())

    @patch('api.search.blockchain_client.client.BlockchainClient.transaction')
    def test_should_create_transaction_search_log(self, mock):
        url = reverse('transaction-detail', kwargs={'crypto': 'bch', 'tx': 'searchlog'})
        mock.return_value = []
        self.assertFalse(TransactionSearch.objects.filter(crypto='bch', transaction='searchlog', creator=self.user).exists())
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertTrue(TransactionSearch.objects.filter(crypto='bch', transaction='searchlog', creator=self.user).exists())

    def test_should_NOT_allow_negative_pages(self):
        url = reverse('address-transactions',
                      kwargs={'crypto': 'bch', 'address': 'qqtgm0njzgctkmhc28q6530zvjs0pjedxq4d4r7qfr'})
        response = self.client.get(url, {'page': -1})
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.data, {'detail': '\'page\' cannot be negative'})
