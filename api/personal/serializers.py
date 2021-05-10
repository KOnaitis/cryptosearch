from rest_framework import fields, serializers


class MyBalanceSerializer(serializers.Serializer):
    balance = fields.IntegerField()
