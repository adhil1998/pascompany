from rest_framework.generics import ListAPIView, ListCreateAPIView, \
    CreateAPIView, RetrieveAPIView


from common.permissions import IsAuthenticated
from common.functions import success_response
from rest_framework.views import APIView
from accounts.serializers import *
from accounts.filter import *
from accounts.models import User, Contact
from transactioins.models import Transaction
from rest_framework.response import Response


# Create your views here.

class UserCreateView(CreateAPIView, RetrieveAPIView):
    """Serializer for lis and create User(s)"""
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserGetView(RetrieveAPIView):
    """Serializer for lis and create User(s)"""
    permission_classes = (IsAuthenticated, )
    serializer_class = UserSerializer
    queryset = User.objects.all()


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
        return success_response({'hiii'}, 'Logout successful', 200)


class ContactListCreateView(ListCreateAPIView):
    """Serializer for lis and create User(s)"""
    permission_classes = (IsAuthenticated,)
    serializer_class = ContactSerializer
    filterset_class = ContactFilter

    def get_queryset(self):
        """Override queryset"""
        user = self.kwargs['user']
        queryset = Contact.objects.filter(user=user)
        return queryset


class ContactListView(ListCreateAPIView):
    """Serializer for lis and create User(s)"""
    permission_classes = (IsAuthenticated,)
    serializer_class = ContactListSerializer
    filterset_class = ContactFilter

    def get_queryset(self):
        """Override queryset"""
        user = self.kwargs['user']
        queryset = Contact.objects.filter(user=user)
        return queryset


class DashboardView(APIView):
    """View for DashboardDetails"""
    permission_classes = (IsAuthenticated,)

    def get(self, request, user=None, *args, **kwargs):
        """Override get method"""
        incomes = Transaction.objects.filter(
            contact__user=user, type=100, parent_transaction=None).annotate(
            child_sum=F('amount') - Sum(
            'child_transactions__amount', default=0)).aggregate(Sum(
            'child_sum'))['child_sum__sum']
        expense = Transaction.objects.filter(
            contact__user=user, type=200, parent_transaction=None).annotate(
            child_sum=F('amount') - Sum(
            'child_transactions__amount', default=0)).aggregate(Sum(
            'child_sum'))['child_sum__sum']
        data = {"name": user.get_full_name(),
                "idencode": user.idencode,
                "Total_income": incomes,
                "incomes_count": Transaction.objects.filter(contact__user=user, type=100).count(),
                "total_expense": expense,
                "expense_count": Transaction.objects.filter(contact__user=user, type=200).count()}
        return Response(data)
