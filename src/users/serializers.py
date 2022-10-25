from django.db.migrations.serializer import BaseSerializer
from rest_framework import serializers

from src.users.models import UserModel


class RegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=128, min_length=8, write_only=True)
    password2 = serializers.CharField(max_length=128, min_length=8, write_only=True)

    class Meta:
        model = UserModel
        fields = ['password1', 'password2', 'username', 'email', 'last_name', 'first_name']

    def create(self, validated_data):
        password = validated_data.pop('password')
        return UserModel.objects.create_user(password=password, **validated_data)


class LoginSerializer(BaseSerializer, serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, min_length=8)
