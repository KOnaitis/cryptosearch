from collections import OrderedDict
from unittest.mock import patch

from django.test import TestCase
from rest_framework.exceptions import NotFound

from api.blockchain_client.client import BlockchainClient


class StubResponse:
    def __init__(self, data, status=200):
        self.data = data
        self.status_code = status

    def json(self):
        return self.data


class TestBlockchainClient(TestCase):
    @patch('requests.get')
    def test_eth_should_parse_address_balance_into_common_format(self, mock):
        mock.return_value = StubResponse({
          "0xaa62dc6cd0123d5bb1e080e61f5fe508b7c8744e": {
            "balance": "5838070680000000000",
            "nonce": 5
          }
        })
        hash = '0xaa62dc6cd0123d5bb1e080e61f5fe508b7c8744e'
        result = BlockchainClient.address_balance('eth', hash)
        mock.assert_called_once_with(f'https://api.blockchain.info/eth/account/{hash}/balance')
        expected = {
            'address': hash,
            'crypto': 'eth',
            'balance': 5838070680000000000
        }
        self.assertDictEqual(result, expected)

    @patch('requests.get')
    def test_eth_should_parse_transaction_into_common_format(self, mock):
        mock.return_value = StubResponse({
            "hash": "0x8d3eb0836e0c73ee60c3d89d06d830f8c31c19f47c1dc6fbfc9e02e20852352b",
            "to": "0xd2c7649ab7ededf965e5bcd0d7007ebeaee179c4",
            "from": "0xaa62dc6cd0123d5bb1e080e61f5fe508b7c8744e",
            "value": "15000000000000000000",
            "nonce": "4",
            "state": "CONFIRMED",
            "timestamp": "1620562387"
        })
        hash = '0x8d3eb0836e0c73ee60c3d89d06d830f8c31c19f47c1dc6fbfc9e02e20852352b'
        result = BlockchainClient.transaction('eth', hash)
        mock.assert_called_once_with(f'https://api.blockchain.info/v2/eth/data/transaction/{hash}')
        expected = OrderedDict([
            ('inputs', [OrderedDict([
                ('address', '0xaa62dc6cd0123d5bb1e080e61f5fe508b7c8744e'),
                ('value', 15000000000000000000)])]),
            ('outputs', [OrderedDict([
                ('address', '0xd2c7649ab7ededf965e5bcd0d7007ebeaee179c4'),
                ('value', 15000000000000000000)])]),
            ('timestamp', '2021-05-09T12:13:07Z')])
        self.assertDictEqual(result, expected)

    @patch('requests.get')
    def test_eth_should_parse_address_transactions_into_common_format(self, mock):
        mock.return_value = StubResponse({'transactions': [
            {
                "hash": "0x8d3eb0836e0c73ee60c3d89d06d830f8c31c19f47c1dc6fbfc9e02e20852352b",
                "to": "0xd2c7649ab7ededf965e5bcd0d7007ebeaee179c4",
                "from": "0xaa62dc6cd0123d5bb1e080e61f5fe508b7c8744e",
                "value": "15000000000000000000",
                "nonce": "4",
                "state": "CONFIRMED",
                "timestamp": "1620562387"
            },
            {
                "blockHash": "0xe1070aa40cedc5ac354ceac48a4f93323b00839d7147623cb4e25648c2c7cf0f",
                "to": "0xd2c7649ab7ededf965e5bcd0d7007ebeaee179c4",
                "from": "0xaa62dc6cd0123d5bb1e080e61f5fe508b7c8744e",
                "value": "1000000000000000000",
                "state": "CONFIRMED",
                "timestamp": "1620562074"
            }
        ]})
        result = BlockchainClient.transactions_for_address('eth', '0xaa62dc6cd0123d5bb1e080e61f5fe508b7c8744e', 1, 30)
        mock.assert_called_once_with(
            'https://api.blockchain.info/v2/eth/data/account/0xaa62dc6cd0123d5bb1e080e61f5fe508b7c8744e/transactions',
            params={'page': 1, 'size': 30})
        expected = OrderedDict([
            ('transactions', [
                OrderedDict([
                    ('inputs', [OrderedDict([
                        ('address', '0xaa62dc6cd0123d5bb1e080e61f5fe508b7c8744e'),
                        ('value', 15000000000000000000)])]),
                    ('outputs', [OrderedDict([
                        ('address', '0xd2c7649ab7ededf965e5bcd0d7007ebeaee179c4'),
                        ('value', 15000000000000000000)])]),
                    ('timestamp', '2021-05-09T12:13:07Z')]),
                OrderedDict([
                    ('inputs', [OrderedDict([
                        ('address', '0xaa62dc6cd0123d5bb1e080e61f5fe508b7c8744e'),
                        ('value', 1000000000000000000)])]),
                    ('outputs', [OrderedDict([
                        ('address', '0xd2c7649ab7ededf965e5bcd0d7007ebeaee179c4'),
                        ('value', 1000000000000000000)])]),
                    ('timestamp', '2021-05-09T12:07:54Z')])])
        ])
        self.assertDictEqual(result, expected)

    @patch('requests.get')
    def test_bch_should_parse_address_balance_into_common_format(self, mock):
        mock.return_value = StubResponse({
          "address": "bitcoincash:qzh0095g66csxg04ms7zhcrg2tludgt3duksgjndts",
          "confirmed": 452481,
          "unconfirmed": 0,
          "utxo": 4,
          "txs": 333,
          "received": 87276583
        })
        hash = 'qzh0095g66csxg04ms7zhcrg2tludgt3duksgjndts'
        result = BlockchainClient.address_balance('bch', hash)
        mock.assert_called_once_with(f'https://api.blockchain.info/haskoin-store/bch/address/{hash}/balance')
        expected = {
            'address': 'bitcoincash:qzh0095g66csxg04ms7zhcrg2tludgt3duksgjndts',
            'crypto': 'bch',
            'balance': 452481
        }
        self.assertDictEqual(result, expected)

    @patch('requests.get')
    def test_bch_should_parse_transaction_into_common_format(self, mock):
        response = {
            "txid": "12e5d4e3091e5f3b7a1729398e084fb9971efbaf082983069427fd180d2d50c5",
            "size": 219,
            "version": 2,
            "locktime": 0,
            "fee": 220,
            "inputs": [{"value": 195673, "address": "bitcoincash:qpld9cdua8aa34hl3dm8xrv37y2ps4dwjura8m3h2y"}],
            "outputs": [
                {"address": None, "value": 735},
                {"address": "bitcoincash:qpld9cdua8aa34hl3dm8xrv37y2ps4dwjura8m3h2y", "value": 194718}
            ],
            "time": 1620561517
        }
        mock.return_value = StubResponse(response)
        hash = '5aaa2ecc901a6d42fa27eb7ca1535df76ffc75416dd54180c4f9034b9c6d4dc5'
        result = BlockchainClient.transaction('bch', hash)
        mock.assert_called_once_with(f'https://api.blockchain.info/haskoin-store/bch/transaction/{hash}')
        expected = OrderedDict([
            ('inputs', [OrderedDict([
                ('address', 'bitcoincash:qpld9cdua8aa34hl3dm8xrv37y2ps4dwjura8m3h2y'),
                ('value', 195673)])]),
            ('outputs', [OrderedDict([
                ('address', None),
                ('value', 735)]),
                OrderedDict([('address', 'bitcoincash:qpld9cdua8aa34hl3dm8xrv37y2ps4dwjura8m3h2y'),
                             ('value', 194718)])]),
            ('timestamp', '2021-05-09T11:58:37Z')
        ])
        self.assertDictEqual(result, expected)

    @patch('requests.get')
    def test_bch_should_parse_address_transactions_into_common_format(self, mock):
        response = [
            {
                "txid": "12e5d4e3091e5f3b7a1729398e084fb9971efbaf082983069427fd180d2d50c5",
                "size": 219,
                "version": 2,
                "locktime": 0,
                "fee": 220,
                "inputs": [{"value": 195673, "address": "bitcoincash:qpld9cdua8aa34hl3dm8xrv37y2ps4dwjura8m3h2y"}],
                "outputs": [
                    {"address": "bitcoincash:qp0lac2exr64laxzuju02jtt0eeg0usp3s7kjf0s2p", "value": 735},
                    {"address": "bitcoincash:qpld9cdua8aa34hl3dm8xrv37y2ps4dwjura8m3h2y", "value": 194718}
                ],
                "time": 1620561517
            },
            {
                "txid": "107e66d9f2016776613fdd782d1927b0dde2b99a77a7cb363924ef321704cdb9",
                "inputs": [{"value": 197360, "address": "bitcoincash:qpld9cdua8aa34hl3dm8xrv37y2ps4dwjura8m3h2y"}],
                "outputs": [
                    {
                        "address": "bitcoincash:prpaa5aggrwhksqh3sz7hyyn5nvmq2zzegu39dppqx",
                        "value": 1469,
                        "spent": False
                    },
                    {
                        "address": "bitcoincash:qpld9cdua8aa34hl3dm8xrv37y2ps4dwjura8m3h2y",
                        "value": 195673,
                        "spent": True,
                        "spender": {
                            "txid": "12e5d4e3091e5f3b7a1729398e084fb9971efbaf082983069427fd180d2d50c5",
                            "input": 0
                        }
                    }
                ],
                "time": 1620561462
            }
        ]
        mock.return_value = StubResponse(response)
        result = BlockchainClient.transactions_for_address('bch', 'qpld9cdua8aa34hl3dm8xrv37y2ps4dwjura8m3h2y', 2, 20)
        mock.assert_called_once_with(
            'https://api.blockchain.info/haskoin-store/bch/address/qpld9cdua8aa34hl3dm8xrv37y2ps4dwjura8m3h2y' +
            '/transactions/full', params={'limit': 20, 'offset': 40})
        expected = OrderedDict([
            ('transactions', [OrderedDict([
                ('inputs', [OrderedDict([
                    ('address', 'bitcoincash:qpld9cdua8aa34hl3dm8xrv37y2ps4dwjura8m3h2y'),
                    ('value', 195673)])]),
                ('outputs', [OrderedDict([
                    ('address', 'bitcoincash:qp0lac2exr64laxzuju02jtt0eeg0usp3s7kjf0s2p'),
                    ('value', 735)]),
                    OrderedDict([('address', 'bitcoincash:qpld9cdua8aa34hl3dm8xrv37y2ps4dwjura8m3h2y'),
                                 ('value', 194718)])]),
                ('timestamp', '2021-05-09T11:58:37Z')
            ]), OrderedDict([
                ('inputs', [OrderedDict([
                    ('address', 'bitcoincash:qpld9cdua8aa34hl3dm8xrv37y2ps4dwjura8m3h2y'),
                    ('value', 197360)])]),
                ('outputs', [OrderedDict([
                    ('address', 'bitcoincash:prpaa5aggrwhksqh3sz7hyyn5nvmq2zzegu39dppqx'),
                    ('value', 1469)]),
                    OrderedDict([
                        ('address', 'bitcoincash:qpld9cdua8aa34hl3dm8xrv37y2ps4dwjura8m3h2y'),
                        ('value', 195673)])]),
                ('timestamp', '2021-05-09T11:57:42Z')])])
        ])
        self.assertDictEqual(result, expected)

    @patch('requests.get')
    def test_btc_should_parse_address_balance_into_common_format(self, mock):
        mock.return_value = StubResponse({
          "address": "bc1q8c0wvzxjfeuzr6xhp7xyxjxjh8r0dsc5ph224d",
          "confirmed": 0,
          "unconfirmed": 0,
          "utxo": 0,
          "txs": 4,
          "received": 562685
        })
        hash = 'bc1q8c0wvzxjfeuzr6xhp7xyxjxjh8r0dsc5ph224d'
        result = BlockchainClient.address_balance('btc', hash)
        mock.assert_called_once_with(f'https://api.blockchain.info/haskoin-store/btc/address/{hash}/balance')
        expected = {
            'address': 'bc1q8c0wvzxjfeuzr6xhp7xyxjxjh8r0dsc5ph224d',
            'crypto': 'btc',
            'balance': 0
        }
        self.assertDictEqual(result, expected)

    @patch('requests.get')
    def test_btc_should_parse_address_transactions_into_common_format(self, mock):
        response = [{
            "inputs": [
                {
                    "output": 0, "sequence": 4294967295, "value": 135974,
                    "address": "bc1q8c0wvzxjfeuzr6xhp7xyxjxjh8r0dsc5ph224d"
                },
                {
                    "output": 2, "sigscript": "", "value": 84574,
                    "address": "bc1q8c0wvzxjfeuzr6xhp7xyxjxjh8r0dsc5ph224d"
                }
            ],
            "outputs": [
                {"address": "1LDXE2o8mJDKcgLjLZStZq2nZXMQaUzdrv", "value": 202992}
            ],
            "time": 1620513287,
            "rbf": False
        }]
        mock.return_value = StubResponse(response)
        result = BlockchainClient.transactions_for_address('btc', 'bc1q8c0wvzxjfeuzr6xhp7xyxjxjh8r0dsc5ph224d', 2, 20)
        mock.assert_called_once_with(
            'https://api.blockchain.info/haskoin-store/btc/address/bc1q8c0wvzxjfeuzr6xhp7xyxjxjh8r0dsc5ph224d' +
            '/transactions/full', params={'limit': 20, 'offset': 40})
        expected = OrderedDict([
            ('transactions', [OrderedDict([
                ('inputs', [OrderedDict([
                    ('address', 'bc1q8c0wvzxjfeuzr6xhp7xyxjxjh8r0dsc5ph224d'),
                    ('value', 135974)]),
                    OrderedDict([
                        ('address', 'bc1q8c0wvzxjfeuzr6xhp7xyxjxjh8r0dsc5ph224d'),
                        ('value', 84574)])]),
                ('outputs', [OrderedDict([
                    ('address', '1LDXE2o8mJDKcgLjLZStZq2nZXMQaUzdrv'),
                    ('value', 202992)])]),
                ('timestamp', '2021-05-08T22:34:47Z')])])
        ])
        self.assertDictEqual(result, expected)

    @patch('requests.get')
    def test_btc_should_parse_transaction_into_common_format(self, mock):
        response = {
            "inputs": [
                {
                    "output": 0, "sequence": 4294967295, "value": 135974,
                    "address": "bc1q8c0wvzxjfeuzr6xhp7xyxjxjh8r0dsc5ph224d"
                },
                {
                    "output": 2, "sigscript": "", "value": 84574,
                    "address": "bc1q8c0wvzxjfeuzr6xhp7xyxjxjh8r0dsc5ph224d"
                }
            ],
            "outputs": [
                {"address": "1LDXE2o8mJDKcgLjLZStZq2nZXMQaUzdrv", "value": 202992}
            ],
            "time": 1620513287,
            "rbf": False
        }
        mock.return_value = StubResponse(response)
        hash = '436b9e8e30592024ce5ea618245fe5eeac3d00cc453af9ca0ecb5611c26f59ef'
        result = BlockchainClient.transaction('btc', hash)
        mock.assert_called_once_with(f'https://api.blockchain.info/haskoin-store/btc/transaction/{hash}')
        expected = OrderedDict([
            ('inputs', [OrderedDict([
                ('address', 'bc1q8c0wvzxjfeuzr6xhp7xyxjxjh8r0dsc5ph224d'),
                ('value', 135974)]),
                OrderedDict([
                    ('address', 'bc1q8c0wvzxjfeuzr6xhp7xyxjxjh8r0dsc5ph224d'),
                    ('value', 84574)])]),
            ('outputs', [OrderedDict([
                ('address', '1LDXE2o8mJDKcgLjLZStZq2nZXMQaUzdrv'),
                ('value', 202992)])]),
            ('timestamp', '2021-05-08T22:34:47Z')])
        self.assertDictEqual(result, expected)

    @patch('requests.get')
    def test_address_balance_should_return_404_when_downstream_returns_404(self, mock):
        mock.return_value = StubResponse({}, 404)
        self.assertRaises(
            NotFound,
            BlockchainClient.address_balance,
            'btc', 'bc1q8c0wvzxjfeuzr6xhp7xyxjxjh8r0dsc5ph224d')

    @patch('requests.get')
    def test_transaction_should_return_404_when_downstream_returns_404(self, mock):
        mock.return_value = StubResponse({}, 404)
        self.assertRaises(
            NotFound,
            BlockchainClient.transaction,
            'bch', '436b9e8e30592024ce5ea618245fe5eeac3d00cc453af9ca0ecb5611c26f59ef')

    @patch('requests.get')
    def test_address_transactions_should_return_404_when_downstream_returns_404(self, mock):
        mock.return_value = StubResponse({}, 404)
        self.assertRaises(NotFound,
                          BlockchainClient.transactions_for_address,
                          'btc', 'bc1q8c0wvzxjfeuzr6xhp7xyxjxjh8r0dsc5ph224d', 2, 20)
