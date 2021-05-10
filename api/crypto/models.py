from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from project.crypto_currencies import CryptoCurrency


UserModel = get_user_model()


class Address(models.Model):
    crypto = models.CharField(max_length=10, choices=[(v.value, v.value) for v in CryptoCurrency])
    address = models.CharField(max_length=200)
    owner = models.ForeignKey(to=get_user_model(), on_delete=models.deletion.CASCADE)

    class Meta:
        # Technically, one address should have one owner, but since this is
        # a search service, assuming that address is only unique for the user.
        unique_together = (('crypto', 'address', 'owner'),)


class AddressSearch(models.Model):
    address = models.CharField(max_length=200)  # TODO: random number, would need to look into hash lengths
    crypto = models.CharField(max_length=10, choices=[(v.value, v.value) for v in CryptoCurrency])
    page = models.IntegerField()
    size = models.IntegerField()
    creator = models.ForeignKey(to=UserModel, on_delete=models.deletion.CASCADE)
    created = models.DateTimeField(default=timezone.now)


class TransactionSearch(models.Model):
    transaction = models.CharField(max_length=200)  # TODO: random number, would need to look into hash lengths
    crypto = models.CharField(max_length=10, choices=[(v.value, v.value) for v in CryptoCurrency])
    creator = models.ForeignKey(to=UserModel, on_delete=models.deletion.CASCADE)
    created = models.DateTimeField(default=timezone.now)
