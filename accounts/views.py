from rest_framework.generics import ListAPIView, ListCreateAPIView, \
    CreateAPIView, RetrieveAPIView

from common.permissions import IsAuthenticated, IsAdmin
from common.functions import success_response
from rest_framework.views import APIView
from accounts.serializers import *
from accounts.filter import *
from accounts.models import User
from rest_framework.response import Response


# Create your views here.

class UserCreateView(CreateAPIView):
    """Serializer for lis and create User(s)"""
    permission_classes = (IsAuthenticated, IsAdmin)
    serializer_class = UserSerializer


class UserGetView(ListAPIView, RetrieveAPIView):
    """Serializer for list and create User(s)"""
    permission_classes = (IsAuthenticated, IsAdmin)
    serializer_class = UserSerializer
    queryset = User.objects.filter(type__in=[201, 301])


class LoginView(CreateAPIView):
    """Serializer for lis and create User(s)"""
    serializer_class = LoginSerializer


class LogoutView(APIView):
    """Serializer for lis and create User(s)"""
    permission_classes = (IsAuthenticated,)
    http_method_names = ['post', ]

    def post(self, request, user=None, *args, **kwargs):
        """Override post method"""
        user.logout()
        return success_response({}, 'Logout successful', 200)

