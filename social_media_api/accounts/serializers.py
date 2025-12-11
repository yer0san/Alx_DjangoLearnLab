from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import CustomUser
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'id', 'username', 'email', 'bio', 'profile_picture', 'followers',
        )
        read_only_fields = ('followers',)

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'bio', 'profile_picture')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid credentials.')
        data['user'] = user
        return data
