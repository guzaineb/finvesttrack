import os
import django
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

# Configure Django AVANT les imports
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()


class TestUserViews(TestCase):
    """Tests pour les endpoints utilisateurs"""
    
    def setUp(self):
        self.client = APIClient()
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            email='test@example.com',
            password='password123',
            username='testuser'
        )
    
    def test_register_endpoint(self):
        """Test endpoint d'inscription"""
        url = reverse('register')
        
        # Cas 1: Inscription réussie
        data = {
            'email': 'new@example.com',
            'username': 'newuser',
            'password': 'ValidPass123!',
            'password_confirm': 'ValidPass123!'
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(self.User.objects.filter(email='new@example.com').exists())
        
        # Cas 2: Données invalides (test rapide)
        invalid_data = data.copy()
        invalid_data['password_confirm'] = 'Different123!'
        
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_login_endpoint(self):
        """Test endpoint de connexion"""
        url = reverse('login')
        
        # Cas 1: Login réussi
        response = self.client.post(url, {
            'email': 'test@example.com',
            'password': 'password123'
        }, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Cas 2: Identifiants invalides
        response = self.client.post(url, {
            'email': 'test@example.com',
            'password': 'wrong'
        }, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_profile_endpoint_authentication(self):
        """Test authentification sur endpoint profil"""
        url = reverse('profile')
        
        # Cas 1: Non authentifié
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Cas 2: Authentifié
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test@example.com')