from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.test import APIClient


class TestAddressTransactions(TestCase):
    client = APIClient()

    @patch('api.search.blockchain_client.client.BlockchainClient.transactions_for_address')
    def test_should_allow_btc(self, mock):
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

    @patch('api.search.blockchain_client.client.BlockchainClient.transactions_for_address')
    def test_should_allow_eth(self, mock):
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

    @patch('api.search.blockchain_client.client.BlockchainClient.transactions_for_address')
    def test_should_allow_bch(self, mock):
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
    def test_should_set_page_to_0_by_default(self, mock):
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

    def test_should_NOT_allow_negative_pages(self):
        url = reverse('address-transactions',
                      kwargs={'crypto': 'bch', 'address': 'qqtgm0njzgctkmhc28q6530zvjs0pjedxq4d4r7qfr'})
        response = self.client.get(url, {'page': -1})
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.data, {'detail': '\'page\' cannot be negative'})
