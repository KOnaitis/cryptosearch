from collections import OrderedDict
from unittest.mock import patch

from django.test import TestCase

from api.search.blockchain_client.client import BlockchainClient


class StubResponse:
    def __init__(self, data):
        self.data = data

    def json(self):
        return self.data


class TestBlockchainClient(TestCase):
    @patch('requests.get')
    def test_eth_should_parse_result_into_common_format(self, mock):
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
    def test_bch_should_parse_result_into_common_format(self, mock):
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
    def test_btc_should_parse_result_into_common_format(self, mock):
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
