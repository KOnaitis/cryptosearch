from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND, \
    HTTP_400_BAD_REQUEST
from rest_framework.test import APIClient

from api.blockchain_client.serializers import AddressWithBalance
from api.crypto.models import Address
from api.crypto.serializers import AddressSerializer


class TestMyAddressViews(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='my-address', password='pass')
        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def tearDown(self):
        self.user.delete()

    def test_list_should_list_my_addresses(self):
        another_user = get_user_model().objects.create(username='my-address-another', password='pass')
        address = 'bc1q8c0wvzxjfeuzr6xhp7xyxjxjh8r0dsc5ph224'
        expected = []
        for i in range(2):
            addr = Address(crypto='btc', address=f'{address}{i}', owner=self.user)
            addr.save()
            expected.append(addr)
        for i in range(5):
            addr = Address(crypto='btc', address=f'{address}{i}', owner=another_user)
            addr.save()
        response = self.client.get(reverse('my-address'))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertListEqual(response.data, AddressSerializer(many=True).to_representation(expected))
        another_user.delete()

    def test_create_should_create_address_for_me(self):
        self.assertFalse(Address.objects.filter(
            owner=self.user,
            address='bc1q8c0wvzxjfeuzr6xhp7xyxjxjh8r0dsc5ph224',
            crypto='btc').exists())
        response = self.client.post(
            reverse('my-address'),
            {'address': 'bc1q8c0wvzxjfeuzr6xhp7xyxjxjh8r0dsc5ph224', 'crypto': 'btc'})
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertTrue(Address.objects.filter(
            owner=self.user,
            address='bc1q8c0wvzxjfeuzr6xhp7xyxjxjh8r0dsc5ph224',
            crypto='btc').exists())

    def test_create_should_NOT_allow_duplicates(self):
        response = self.client.post(
            reverse('my-address'),
            {'address': 'bc1q8c0wvzxjfeuzr6xhp7xyxjxjh8r0dsc5ph224', 'crypto': 'btc'})
        self.client.post(
            reverse('my-address'),
            {'address': 'bc1q8c0wvzxjfeuzr6xhp7xyxjxjh8r0dsc5ph224', 'crypto': 'btc'})
        duplicate = self.client.post(
            reverse('my-address'),
            {'address': 'bc1q8c0wvzxjfeuzr6xhp7xyxjxjh8r0dsc5ph224', 'crypto': 'btc'})
        self.assertTrue(response.status_code, HTTP_200_OK)
        self.assertEqual(duplicate.status_code, HTTP_400_BAD_REQUEST)
        self.assertDictEqual(duplicate.data,
                             {'non_field_errors': ['The fields crypto, address, owner must make a unique set.']})

    def test_delete_should_delete_my_address(self):
        addr = Address(crypto='btc', address='bc1q8c0wvzxjfeuzr6xhp7xyxjxjh8r0dsc5ph224', owner=self.user)
        addr.save()
        self.assertTrue(Address.objects.filter(pk=addr.pk).exists())
        url = reverse('my-address-detail', kwargs={'address': 'bc1q8c0wvzxjfeuzr6xhp7xyxjxjh8r0dsc5ph224'})
        response = self.client.delete(url + '?crypto=btc')  # Passing data query params don't work with delete..
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
        self.assertFalse(Address.objects.filter(pk=addr.pk).exists())

    def test_delete_should_return_404_if_address_does_not_exist(self):
        url = reverse('my-address-detail', kwargs={'address': 'bc1q8c0wvzxjfeuzr6xhp7xyxjxjh8r0dsc5ph224'})
        response = self.client.delete(url + '?crypto=btc')  # Passing data query params don't work with delete..
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    @patch('api.blockchain_client.client.BlockchainClient.address_balance')
    def test_my_balance_should_show_list_of_my_addresses_with_balances(self, mock):
        another_user = get_user_model().objects.create(username='my-address-another', password='pass')
        Address(crypto='btc', address='bc1q8c0wvzxjfeuzr6xhp7xyxjxjh8r0dsc5ph224d', owner=self.user).save()
        Address(crypto='bch', address='qqtgm0njzgctkmhc28q6530zvjs0pjedxq4d4r7qfr', owner=another_user).save()
        mock.return_value = AddressWithBalance().to_representation({
            'crypto': 'btc',
            'address': 'bc1q8c0wvzxjfeuzr6xhp7xyxjxjh8r0dsc5ph224d',
            'balance': 1000})
        response = self.client.get(reverse('my-balance'))
        mock.assert_called_once_with(crypto='btc', address='bc1q8c0wvzxjfeuzr6xhp7xyxjxjh8r0dsc5ph224d')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertListEqual(response.data, [{
            'address': 'bc1q8c0wvzxjfeuzr6xhp7xyxjxjh8r0dsc5ph224d',
            'crypto': 'btc',
            'balance': 1000}])

    def test_my_balance_should_return_empty_list_if_no_balances_exist(self):
        response = self.client.get(reverse('my-balance'))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertListEqual(response.data, [])
