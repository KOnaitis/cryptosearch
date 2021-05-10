from rest_framework.generics import DestroyAPIView, ListCreateAPIView
from rest_framework.views import APIView

from api.addresses.models import Address
from api.addresses.serializers import AddressSerializer
from api.personal.serializers import MyBalanceSerializer


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
    def get(self, queryset):
        return MyBalanceSerializer().to_representation({'balance': 0})
