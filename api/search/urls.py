from django.conf.urls import re_path

from .views import AddressTransactionsView, TransactionsView, AddressSearchView, TransactionSearchView

urlpatterns = [
    re_path(r'(?P<crypto>(btc|eth|bch))/address/(?P<address>\w+)/transactions/$', AddressTransactionsView.as_view(),
            name='address-transactions'),
    re_path(r'log/address/$', AddressSearchView.as_view(), name='address-transactions-log'),
    re_path(r'(?P<crypto>(btc|eth|bch))/transaction/(?P<tx>\w+)/$', TransactionsView.as_view(),
            name='transaction-detail'),
    re_path(r'log/transaction/$', TransactionSearchView.as_view(), name='transaction-log'),
]
