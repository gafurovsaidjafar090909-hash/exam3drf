from django.contrib.auth.models import User
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField()
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
    def create(self, validated_data):
        return User.objects.create_user(username=validated_data['username'],password=validated_data['password'])


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
        read_only_fields = ['id', 'username']