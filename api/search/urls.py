from django.conf.urls import url

from .views import AddressTransactionsView

urlpatterns = [
    url(r'(?P<crypto>(btc|eth|bch))/address/(?P<address>\w+)/transactions/$', AddressTransactionsView.as_view(), name='address-search'),
]
