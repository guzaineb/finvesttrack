import os
import django
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

# Configure Django AVANT les imports
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.services import AuthService


class TestAuthService(TestCase):
    """Tests pour le service d'authentification"""
    
    def setUp(self):
        self.User = get_user_model()
        self.user_data = {
            'email': 'test@example.com',
            'password': 'SecurePass123!',
            'username': 'testuser'
        }
    
    def test_create_user_success(self):
        """Test création user avec validation métier"""
        user = AuthService.create_user(**self.user_data)
        
        self.assertEqual(user.email, self.user_data['email'])
        self.assertTrue(user.check_password(self.user_data['password']))
        self.assertEqual(user.username, self.user_data['username'])
    
    def test_create_user_duplicate_email(self):
        """Test unicité email (règle métier)"""
        AuthService.create_user(**self.user_data)
        
        with self.assertRaises(ValueError) as ctx:
            AuthService.create_user(**self.user_data)
        
        self.assertIn("existe déjà", str(ctx.exception))
    
    def test_authenticate_user_all_cases(self):
        """Test toutes les règles d'authentification"""
        # Créer user
        AuthService.create_user(**self.user_data)
        
        # Cas 1: Succès
        user = AuthService.authenticate_user(
            email=self.user_data['email'],
            password=self.user_data['password']
        )
        self.assertIsNotNone(user)
        
        # Cas 2: Mauvais password
        user = AuthService.authenticate_user(
            email=self.user_data['email'],
            password='wrong'
        )
        self.assertIsNone(user)
        
        # Cas 3: User inexistant
        user = AuthService.authenticate_user(
            email='nonexistent@example.com',
            password='anything'
        )
        self.assertIsNone(user)
    
    def test_generate_tokens_if_needed(self):
        """Test tokens JWT (si utilisé dans votre app)"""
        user = AuthService.create_user(**self.user_data)
        tokens = AuthService.generate_tokens(user)
        
        if tokens:  # Si vous utilisez JWT
            self.assertIn('access', tokens)
            self.assertIn('refresh', tokens)