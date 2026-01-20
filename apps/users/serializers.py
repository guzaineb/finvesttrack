from rest_framework import serializers
from django.contrib.auth import password_validation
from apps.users.models import User
from apps.users.services import AuthService

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password_confirm']
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas")
        password_validation.validate_password(data['password'])
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        return AuthService.create_user(**validated_data)

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        user = AuthService.authenticate_user(
            email=data['email'],
            password=data['password']
        )
        if not user:
            raise serializers.ValidationError("Identifiants invalides")
        
        data['user'] = user
        return data

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'created_at']