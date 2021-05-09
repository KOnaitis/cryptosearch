from django.contrib.auth import get_user_model
from django.db import models

from api.search.crypto_currencies import CryptoCurrency


UserModel = get_user_model()


class AddressSearch(models.Model):
    address = models.CharField(max_length=200)  # TODO: random number, would need to look into hash lengths
    crypto = models.CharField(max_length=10, choices=[(v.value, v.value) for v in CryptoCurrency])
    page = models.IntegerField()
    size = models.IntegerField()
    # creator = models.ForeignKey(to=UserModel, on_delete=models.deletion.CASCADE)


class TransactionSearch(models.Model):
    transaction = models.CharField(max_length=200)  # TODO: random number, would need to look into hash lengths
    crypto = models.CharField(max_length=10, choices=[(v.value, v.value) for v in CryptoCurrency])
    # creator = models.ForeignKey(to=UserModel, on_delete=models.deletion.CASCADE)
