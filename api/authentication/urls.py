from django.conf.urls import re_path

from .views import RegisterView, LoginView

urlpatterns = [
    re_path(r'register/$', RegisterView.as_view(), name='auth-register'),
    re_path(r'login/$', LoginView.as_view(), name='auth-login'),
]
