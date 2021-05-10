from django.conf.urls import re_path

from .views import MyAddressView, MyAddressDestroyView, MyBalanceView

urlpatterns = [
    re_path(r'addresses/$', MyAddressView.as_view(), name='my-address'),
    re_path(r'addresses/(?P<address>\w+)/$', MyAddressDestroyView.as_view(), name='my-address-detail'),
    re_path(r'balance/$', MyBalanceView.as_view(), name='my-balance')
]
