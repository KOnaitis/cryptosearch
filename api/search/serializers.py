from rest_framework.serializers import Serializer, CharField, IntegerField, DateTimeField


class TransactionOutputSerializer(Serializer):
    address = CharField()
    value = IntegerField()


class TransactionInputSerializer(Serializer):
    address = CharField()
    value = IntegerField()


class TransactionSerializer(Serializer):
    inputs = TransactionInputSerializer(many=True)
    outputs = TransactionOutputSerializer(many=True)
    timestamp = DateTimeField()


class TransactionsSerializer(Serializer):
    transactions = TransactionSerializer(many=True)
