from django.conf.urls import re_path

from .views import AddressTransactionsView, TransactionsView, AddressSearchView, TransactionSearchView

urlpatterns = [
    re_path(r'(?P<crypto>(btc|eth|bch))/addresses/(?P<address>\w+)/transactions/$', AddressTransactionsView.as_view(),
            name='address-transactions'),
    re_path(r'searches/addresses/$', AddressSearchView.as_view(), name='address-transactions-log'),
    re_path(r'(?P<crypto>(btc|eth|bch))/transactions/(?P<tx>\w+)/$', TransactionsView.as_view(),
            name='transaction-detail'),
    re_path(r'searches/transactions/$', TransactionSearchView.as_view(), name='transaction-log'),
]
