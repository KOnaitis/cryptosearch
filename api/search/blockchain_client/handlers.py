from datetime import datetime

import requests
from rest_framework.exceptions import NotFound, APIException
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from api.search.serializers import TransactionsSerializer

HASKOIN_BASE = 'https://api.blockchain.info/haskoin-store'
V2_BASE = 'https://api.blockchain.info/v2'


def page_to_offset(page, size):
    return page * size


class CryptoHandler:
    def transform_transactions(self, data):
        raise NotImplementedError('Not implemented')

    def query_transactions_by_address(self, address, page, size):
        raise NotImplementedError('Not implemented')

    def transactions_by_address(self, address, page, size):
        response = self.query_transactions_by_address(address, page, size)
        if response.status_code == HTTP_404_NOT_FOUND:
            # TODO: This doesn't work too well with ETH, since that API returns empty list with 404
            raise NotFound(f'Address \'{address}\' does not exist.')
        elif response.status_code != HTTP_200_OK:
            # TODO: ideally, would have more granular checks here.
            #       Most likely in a method so that specific handlers could override the logic.
            raise APIException(f'Failed to retrieve data for address \'{address}\'')
        transformed = self.transform_transactions(response.json())
        serializer = TransactionsSerializer(data={'transactions': transformed})
        serializer.is_valid(raise_exception=True)
        return serializer.data


class ETHHandler(CryptoHandler):
    def query_transactions_by_address(self, address, page, size):
        return requests.get(f'{V2_BASE}/eth/data/account/{address}/transactions',
                            params={'page': page, 'size': size})

    def transform_transactions(self, data):
        transformed = []
        for tx in data['transactions']:
            transformed.append({
                'inputs': [{'address': tx['from'], 'value': tx['value']}],
                'outputs': [{'address': tx['to'], 'value': tx['value']}],
                'timestamp': datetime.fromtimestamp(int(tx['timestamp']))
            })
        return transformed


class BCHHandler(CryptoHandler):
    def query_transactions_by_address(self, address, page, size):
        offset = page_to_offset(page, size)
        return requests.get(
            f'{HASKOIN_BASE}/bch/address/{address}/transactions/full',
            params={'limit': size, 'offset': offset})

    def transform_transactions(self, data):
        for tx in data:
            tx['timestamp'] = datetime.fromtimestamp(tx['time'])
        return data


class BTCHandler(CryptoHandler):
    def query_transactions_by_address(self, address, page, size):
        offset = page_to_offset(page, size)
        return requests.get(
            f'{HASKOIN_BASE}/btc/address/{address}/transactions/full',
            params={'limit': size, 'offset': offset})

    def transform_transactions(self, data):
        for tx in data:
            tx['timestamp'] = datetime.fromtimestamp(tx['time'])
        return data
