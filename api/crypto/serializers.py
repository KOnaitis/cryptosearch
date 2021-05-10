from rest_framework.serializers import ModelSerializer

from .models import AddressSearch, TransactionSearch, Address


class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
        extra_kwargs = {'owner': {'write_only': True}}


class AddressSearchSerializer(ModelSerializer):
    class Meta:
        model = AddressSearch
        fields = '__all__'


class TransactionSearchSerializer(ModelSerializer):
    class Meta:
        model = TransactionSearch
        fields = '__all__'
