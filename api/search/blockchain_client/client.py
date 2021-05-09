from rest_framework.exceptions import ParseError, ValidationError

from api.search.blockchain_client.cryptocurrency import CryptoCurrency
from api.search.blockchain_client.handlers import BTCHandler, BCHHandler, ETHHandler


class BlockchainClient:
    # In general, I'm not sure it's a very good solution, since most likely all currencies cannot be fit into one format
    # But for these 3 and limited requirements it seems to be possible. It's also simpler for the clients of the API.
    handlers = {
        CryptoCurrency.BTC.value: BTCHandler(),
        CryptoCurrency.BCH.value: BCHHandler(),
        CryptoCurrency.ETH.value: ETHHandler(),
    }

    @staticmethod
    def transactions_for_address(crypto, address, page, size):
        if page < 0:
            raise ParseError('\'page\' cannot be negative')

        if crypto in BlockchainClient.handlers:
            return BlockchainClient.handlers[crypto].transactions_for_address(address, page, size)

        raise ValidationError(f'Cryptocurrency \'{crypto}\' is not supported')
