from rest_framework import serializers
from .models import User,openaccount,depositetype,applyloan,heroImages
from django.contrib.auth.models import Group


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), many=True)

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'phone', 'pan', 'aadhar', 'photo', 'aadharimg', 'panimg', 'user_type', 'groups')

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model=openaccount
        fields='__all__'

class DepositeSerializer(serializers.ModelSerializer):
    class Meta:
        model=depositetype
        fields='__all__'

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model=applyloan
        fields='__all__'


class HeroImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=heroImages
        fields='__all__'