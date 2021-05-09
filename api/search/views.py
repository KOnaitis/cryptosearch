from django.http import JsonResponse

from rest_framework.views import APIView

from api.search.blockchain_client import BlockchainClient


class AddressTransactionsView(APIView):

    # Locking page size for simplicity
    page_size = 50
    page_query_param = 'page'

    def get(self, request, *args, **kwargs):
        page = request.query_params.get(self.page_query_param, 0)
        crypto = kwargs.get('crypto')
        address = kwargs.get('address')
        return JsonResponse(
            BlockchainClient.transactions_for_address(crypto=crypto, address=address, page=page, size=self.page_size),
            safe=False)
