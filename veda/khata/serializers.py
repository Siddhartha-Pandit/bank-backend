from rest_framework import serializers
from .models import User,openaccount,depositetype,applyloan,heroImages
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password


# class UserSerializer(serializers.ModelSerializer):
#     groups = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), many=True)

#     class Meta:
#         model = User
#         fields = '__all__'
#         # fields = ('id', 'name', 'email', 'phone', 'pan', 'aadhar', 'photo', 'aadharimg', 'panimg', 'user_type', 'groups')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'phone', 'pan', 'aadhar', 'photo', 'aadharimg', 'panimg', 'user_type', 'password']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

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

class VerificationSerializer(serializers.Serializer):
    token = serializers.UUIDField()

    def validate_token(self, value):
        try:
            user = User.objects.get(verification_token=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid token")
        if user.is_verified:
            raise serializers.ValidationError("Account already verified")
        return value