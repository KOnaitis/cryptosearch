from rest_framework import permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model

from .serializers import UserSerializer


class RegisterView(CreateAPIView):
    model = get_user_model()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer


class LoginView(ObtainAuthToken):
    permission_classes = (permissions.AllowAny,)
