from typing import Dict, Optional
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.models import User

class AuthService:
    """Service dédié à l'authentification (principe SRP)"""
    
    @staticmethod
    def create_user(email: str, password: str, **extra_fields) -> User:
        """Crée un nouvel utilisateur avec validation"""
        if User.objects.filter(email=email).exists():
            raise ValueError("Un utilisateur avec cet email existe déjà")
        
        user = User.objects.create_user(
            email=email,
            password=password,
            **extra_fields
        )
        return user
    
    @staticmethod
    def authenticate_user(email: str, password: str) -> Optional[User]:
        """Authentifie un utilisateur"""
        user = authenticate(username=email, password=password)
        return user
    
    @staticmethod
    def generate_tokens(user: User) -> Dict[str, str]:
        """Génère les tokens JWT"""
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }