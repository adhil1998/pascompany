from rest_framework import serializers
from django.db.models import Sum, F
from django.contrib.auth import authenticate

from common.exceptions import UnauthorizedAccess
from common.fields import KWArgsObjectField
from accounts.models import User, Contact
from accounts.utilities import upload_image_and_get_url
from transactioins.models import Transaction


class UserSerializer(serializers.ModelSerializer):
    """Serializer for lis and create User(s)"""
    profile_pic = serializers.ImageField(write_only=True, required=False)

    class Meta:
        """meta info"""
        model = User
        fields = ['username', 'idencode', 'email', 'dob', 'phone_number',
                  'password', 'first_name', 'last_name', 'profile_pic']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        """Override user creation"""
        if 'profile_pic' in validated_data.keys():
            validated_data['profile_pic'] = upload_image_and_get_url(
                validated_data.pop('profile_pic'),
                validated_data['first_name'] + validated_data['last_name'])
        password = validated_data.pop('password')
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(password)
        user.save()
        return user

    def to_representation(self, instance):
        """Override output"""
        data = super(UserSerializer, self).to_representation(instance)
        data['profile_pic'] = instance.profile_pic
        return data


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def create(self, validated_data):
        """Overide login"""
        username = validated_data['username']
        password = validated_data['password']
        user = authenticate(username=username, password=password)
        if not user:
            raise UnauthorizedAccess('Not valid credentials')
        return user

    def to_representation(self, instance):
        """Override instance output"""
        data = {
            "idencode": instance.idencode,
            "name": instance.username,
            "bearer": instance.issue_access_token(),
        }
        return data


class ContactSerializer(serializers.ModelSerializer):
    """Serializer for contacts"""
    user = KWArgsObjectField()
    transactions_detail = serializers.SerializerMethodField(read_only=True)
    image = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = Contact
        fields = ['name', 'phone', 'address', 'idencode',
                  'user', 'transactions_detail', 'image']

    def get_transactions_detail(self, obj):
        """Method for get transaction details with a contact"""
        total_income = Transaction.objects.filter(
            contact=obj, type=100, parent_transaction=None).annotate(
            child_sum=F('amount') - Sum(
            'child_transactions__amount', default=0)).aggregate(
            Sum('child_sum', default=0))['child_sum__sum']
        total_expense = Transaction.objects.filter(
            contact=obj, type=200, parent_transaction=None).annotate(
            child_sum=F('amount') - Sum(
            'child_transactions__amount', default=0)).aggregate(
            Sum('child_sum', default=0))['child_sum__sum']
        if total_income >= total_expense:
            data = {"amount": total_income - total_expense,
                    'type': 100}
        else:
            data = {"amount": total_expense - total_income,
                    'type': 200}
        return data

    def create(self, validated_data):
        """Override create"""
        if 'image' in validated_data.keys():
            validated_data['image'] = upload_image_and_get_url(
                validated_data.pop('image'), validated_data['name'])
        validated_data['user'] = self.context['view'].kwargs['user']
        contact = super(ContactSerializer, self).create(validated_data)
        return contact

    def to_representation(self, instance):
        """Override output"""
        data = super(ContactSerializer, self).to_representation(instance)
        data['image'] = instance.image
        return data


class ContactListSerializer(serializers.ModelSerializer):
    """Serializer for contacts"""

    class Meta:
        model = Contact
        fields = ['name', 'idencode']
