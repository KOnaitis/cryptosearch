from django.contrib.auth import get_user_model
from django.db import models

from api.search.crypto_currencies import CryptoCurrency


class Address(models.Model):
    crypto = models.CharField(max_length=10, choices=[(v.value, v.value) for v in CryptoCurrency])
    address = models.CharField(max_length=200)
    owner = models.ForeignKey(to=get_user_model(), on_delete=models.deletion.CASCADE)

    class Meta:
        # Technically, one address should have one owner, but since this is
        # a search service, assuming that address is only unique for the user.
        unique_together = (('crypto', 'address', 'owner'),)
