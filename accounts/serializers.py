from rest_framework import serializers
from django.db.models import Sum, F
from django.contrib.auth import authenticate

from common.exceptions import UnauthorizedAccess
from common.fields import KWArgsObjectField
from accounts.models import User
from accounts.utilities import upload_image_and_get_url


class UserSerializer(serializers.ModelSerializer):
    """Serializer for lis and create User(s)"""
    profile_pic = serializers.ImageField(write_only=True, required=False)
    aadhar = serializers.ImageField(write_only=True, required=False)

    class Meta:
        """meta info"""
        model = User
        fields = ['username', 'idencode', 'email', 'dob', 'phone_number',
                  'password', 'first_name', 'last_name', 'profile_pic', 'type',
                  'aadhar']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        """Override user creation"""
        if 'profile_pic' in validated_data.keys():
            validated_data['profile_pic'] = upload_image_and_get_url(
                validated_data.pop('profile_pic'),
                validated_data['first_name'] + validated_data['last_name'])
        if 'aadhar' in validated_data.keys():
            validated_data['aadhar'] = upload_image_and_get_url(
                validated_data.pop('aadhar'),
                validated_data['first_name'] + validated_data['last_name'] +
                'aadhar')
        password = validated_data.pop('password')
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(password)
        user.save()
        return user

    def to_representation(self, instance):
        """Override output"""
        data = super(UserSerializer, self).to_representation(instance)
        data['profile_pic'] = instance.profile_pic
        data['aadhar'] = instance.aadhar
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
            "type": instance.type
        }
        return data
