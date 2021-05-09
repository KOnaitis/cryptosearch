from enum import Enum

import requests

import logging
logger = logging.getLogger(__name__)


HASKOIN_BASE = 'https://api.blockchain.info/haskoin-store'
V2_BASE = 'https://api.blockchain.info/v2'


class CryptoCurrency(Enum):
    BTC = 'btc'
    ETH = 'eth'
    BCH = 'bch'


class BlockchainClient:
    @staticmethod
    def transactions_for_address(crypto, address, page, size):
        retrievers = {
            CryptoCurrency.BTC.value: BlockchainClient.btc_transactions,
            CryptoCurrency.BCH.value: BlockchainClient.bch_transactions,
            CryptoCurrency.ETH.value: BlockchainClient.eth_transactions,
        }
        if crypto in retrievers:
            return retrievers[crypto](address, page, size)
        raise ValueError(f'Cryptocurrency \'{crypto}\' is not supported')

    @staticmethod
    def eth_transactions(address, page, size):
        response = requests.get(
            f'{V2_BASE}/eth/data/account/{address}/transactions?page={page}&size={size}').json()
        logger.info(response)
        return response

    @staticmethod
    def btc_transactions(address, page, size):
        offset = BlockchainClient.__page_to_offset(page, size)
        response = requests.get(
            f'{HASKOIN_BASE}/btc/address/{address}/transactions/full?limit={size}&offset={offset}').json()
        logger.info(response)
        return response

    @staticmethod
    def bch_transactions(address, page, size):
        offset = BlockchainClient.__page_to_offset(page, size)
        response = requests.get(
            f'{HASKOIN_BASE}/bch/address/{address}/transactions/full?limit={size}&offset={offset}').json()
        logger.info(response)
        return response

    @staticmethod
    def __page_to_offset(page, size):
        return page * size
