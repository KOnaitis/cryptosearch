from rest_framework.fields import CharField, IntegerField, DateTimeField
from rest_framework.serializers import Serializer


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


class AddressWithBalance(Serializer):
    crypto = CharField()
    address = CharField()
    balance = IntegerField()
