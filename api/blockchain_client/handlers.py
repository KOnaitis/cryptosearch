import logging
from datetime import datetime

import requests
from rest_framework.exceptions import NotFound, APIException
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from project.crypto_currencies import CryptoCurrency
from .serializers import TransactionsSerializer, TransactionSerializer, AddressWithBalance

BLOCKCHAIN_INFO_BASE = 'https://api.blockchain.info'
HASKOIN_BASE = 'https://api.blockchain.info/haskoin-store'
V2_BASE = 'https://api.blockchain.info/v2'


def page_to_offset(page, size):
    return page * size


class CryptoHandler:
    def transform_address_balance(self, data):
        raise NotImplementedError('Not implemented')

    def transform_transaction(self, tx):
        raise NotImplementedError('Not implemented')

    def transform_transactions(self, data):
        raise NotImplementedError('Not implemented')

    def query_transaction(self, tx):
        raise NotImplementedError('Not implemented')

    def query_address_balance(self, address):
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

    def transaction(self, tx):
        response = self.query_transaction(tx)
        if response.status_code == HTTP_404_NOT_FOUND:
            raise NotFound(f'Transaction \'{tx}\' does not exist.')
        elif response.status_code != HTTP_200_OK:
            # TODO: ideally, would have more granular checks here.
            #       Most likely in a method so that specific handlers could override the logic.
            raise APIException(f'Failed to retrieve data for transaction \'{tx}\'')
        transformed = self.transform_transaction(response.json())
        serializer = TransactionSerializer(data=transformed)
        serializer.is_valid(raise_exception=True)
        return serializer.data

    def address_balance(self, address):
        response = self.query_address_balance(address)
        if response.status_code == HTTP_404_NOT_FOUND:
            raise NotFound(f'Address \'{address}\' does not exist.')
        elif response.status_code != HTTP_200_OK:
            # TODO: ideally, would have more granular checks here.
            #       Most likely in a method so that specific handlers could override the logic.
            raise APIException(f'Failed to retrieve balance for address \'{address}\'')
        transformed = self.transform_address_balance(response.json())
        serializer = AddressWithBalance(data=transformed)
        serializer.is_valid(raise_exception=True)
        return serializer.data


class ETHHandler(CryptoHandler):
    def query_transaction(self, tx):
        return requests.get(f'{V2_BASE}/eth/data/transaction/{tx}')

    def query_address_balance(self, address):
        return requests.get(f'{BLOCKCHAIN_INFO_BASE}/eth/account/{address}/balance')

    def query_transactions_by_address(self, address, page, size):
        return requests.get(f'{V2_BASE}/eth/data/account/{address}/transactions',
                            params={'page': page, 'size': size})

    def transform_address_balance(self, data):
        logging.info(data)
        logging.info(data.items())
        address = list(data.keys())[0]
        return {
            'address': address,
            'balance': int(data[address]['balance']),
            'crypto': CryptoCurrency.ETH.value
        }

    def transform_transaction(self, tx):
        return {
            'inputs': [{'address': tx['from'], 'value': tx['value']}],
            'outputs': [{'address': tx['to'], 'value': tx['value']}],
            'timestamp': datetime.fromtimestamp(int(tx['timestamp']))
        }

    def transform_transactions(self, data):
        transformed = []
        for tx in data['transactions']:
            transformed.append(self.transform_transaction(tx))
        return transformed


class BCHHandler(CryptoHandler):
    # TODO: BTC & BCH handlers could be cleaned up since they use the same API.
    #       APIs should be implemented separately. And then for crypto you should select the API.

    def query_address_balance(self, address):
        return requests.get(f'{HASKOIN_BASE}/bch/address/{address}/balance')

    def query_transaction(self, tx):
        return requests.get(f'{HASKOIN_BASE}/bch/transaction/{tx}')

    def query_transactions_by_address(self, address, page, size):
        offset = page_to_offset(page, size)
        return requests.get(
            f'{HASKOIN_BASE}/bch/address/{address}/transactions/full',
            params={'limit': size, 'offset': offset})

    def transform_address_balance(self, data):
        return {
            'crypto': CryptoCurrency.BCH.value,
            'address': data['address'],
            'balance': data['confirmed']
        }

    def transform_transaction(self, tx):
        return {
            'inputs': tx['inputs'],
            'outputs': tx['outputs'],
            'timestamp': datetime.fromtimestamp(tx['time'])
        }

    def transform_transactions(self, data):
        return [self.transform_transaction(tx) for tx in data]


class BTCHandler(CryptoHandler):
    def query_address_balance(self, address):
        return requests.get(f'{HASKOIN_BASE}/btc/address/{address}/balance')

    def query_transaction(self, tx):
        return requests.get(f'{HASKOIN_BASE}/btc/transaction/{tx}')

    def query_transactions_by_address(self, address, page, size):
        offset = page_to_offset(page, size)
        return requests.get(
            f'{HASKOIN_BASE}/btc/address/{address}/transactions/full',
            params={'limit': size, 'offset': offset})

    def transform_address_balance(self, data):
        return {
            'crypto': CryptoCurrency.BTC.value,
            'address': data['address'],
            'balance': data['confirmed']
        }

    def transform_transaction(self, tx):
        return {
            'inputs': tx['inputs'],
            'outputs': tx['outputs'],
            'timestamp': datetime.fromtimestamp(tx['time'])
        }

    def transform_transactions(self, data):
        return [self.transform_transaction(tx) for tx in data]
