from rest_framework.serializers import Serializer, CharField, IntegerField, DateTimeField, ModelSerializer

from api.search.models import AddressSearch, TransactionSearch


class TransactionOutputSerializer(Serializer):
    address = CharField(allow_null=True)
    value = IntegerField()


class TransactionInputSerializer(Serializer):
    address = CharField(allow_null=True)
    value = IntegerField()


class TransactionSerializer(Serializer):
    inputs = TransactionInputSerializer(many=True)
    outputs = TransactionOutputSerializer(many=True)
    timestamp = DateTimeField()


class TransactionsSerializer(Serializer):
    transactions = TransactionSerializer(many=True)


class AddressSearchSerializer(ModelSerializer):
    class Meta:
        model = AddressSearch
        fields = '__all__'


class TransactionSearchSerializer(ModelSerializer):
    class Meta:
        model = TransactionSearch
        fields = '__all__'
