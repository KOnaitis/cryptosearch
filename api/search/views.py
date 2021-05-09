from rest_framework.response import Response

from rest_framework.views import APIView

from api.search.blockchain_client.client import BlockchainClient


class AddressTransactionsView(APIView):

    # Locking page size for simplicity
    page_size = 50
    page_query_param = 'page'

    def get(self, request, *args, **kwargs):
        page = int(request.query_params.get(self.page_query_param, 0))
        crypto = kwargs.get('crypto')
        address = kwargs.get('address')

        # TODO: would do extra validations on address here, but don't know enough about addresses to do it right now.

        transactions = BlockchainClient.transactions_for_address(
            crypto=crypto,
            address=address,
            page=page,
            size=self.page_size
        )
        return Response(transactions)
