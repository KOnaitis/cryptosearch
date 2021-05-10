import logging

from rest_framework.generics import DestroyAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from api.blockchain_client.client import BlockchainClient
from api.crypto.models import Address
from api.crypto.serializers import AddressSerializer


class MyAddressView(ListCreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def filter_queryset(self, queryset):
        return queryset.filter(owner=self.request.user)

    def get_serializer(self, *args, **kwargs):
        if self.request.method == 'POST':
            data = self.request.data.copy()
            data['owner'] = self.request.user.pk
            kwargs['data'] = data
        return super().get_serializer(*args, **kwargs)


class MyAddressDestroyView(DestroyAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    lookup_url_kwarg = 'address'
    lookup_field = 'address'

    def filter_queryset(self, queryset):
        return queryset.filter(owner=self.request.user, crypto=self.request.query_params.get('crypto'))


class MyBalanceView(APIView):
    # Should be paginated
    def get(self, *args, **kwargs):
        result = []
        for address in Address.objects.filter(owner=self.request.user):  # Could have this in custom object manager
            logging.info(f'{address.address} {address.crypto}')
            result.append(BlockchainClient.address_balance(crypto=address.crypto, address=address.address))
        return Response(data=result)
