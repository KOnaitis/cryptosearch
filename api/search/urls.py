from django.conf.urls import re_path

from .views import AddressTransactionsView

urlpatterns = [
    re_path(r'(?P<crypto>(btc|eth|bch))/address/(?P<address>\w+)/transactions/$', AddressTransactionsView.as_view(),
            name='address-transactions'),
]
