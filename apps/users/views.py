from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenRefreshView
from apps.users.serializers import (
    UserRegisterSerializer,
    UserLoginSerializer,
    UserProfileSerializer
)
from apps.users.services import AuthService

class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        return Response({
            'user': UserProfileSerializer(user).data,
            'message': 'Utilisateur créé avec succès'
        }, status=status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        tokens = AuthService.generate_tokens(user)
        return Response({
            'user': UserProfileSerializer(user).data,
            'tokens': tokens
        })

class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    
    def get_object(self):
        return self.request.user

class CustomTokenRefreshView(TokenRefreshView):
    """Extension possible pour le refresh token si nécessaire"""
    pass