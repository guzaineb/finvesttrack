import pytest
from datetime import date
from decimal import Decimal
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.portfolio.models import Asset

User = get_user_model()


@pytest.mark.django_db
class TestPortfolioViews:
    """Tests pour les vues de l'API"""
    
    def setup_method(self):
        """Setup avant chaque test"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='views@example.com',
            password='password123'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_get_empty_portfolio_summary(self):
        """Test GET /api/portfolio/summary avec portfolio vide"""
        response = self.client.get('/api/portfolio/summary/')
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['total_value'] == 0
        assert data['asset_count'] == 0
    
    def test_create_asset(self):
        """Test POST /api/portfolio/assets/"""
        data = {
            'asset_type': 'STOCK',
            'symbol': 'GOOGL',
            'name': 'Alphabet Inc.',
            'quantity': 5.0,
            'purchase_price': 150.50,
            'current_price': 160.25,
            'purchase_date': '2024-01-15'
        }
        
        response = self.client.post('/api/portfolio/assets/', data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()
        assert response_data['symbol'] == 'GOOGL'
        assert response_data['asset_type'] == 'STOCK'
    
    def test_get_assets_list(self):
        """Test GET /api/portfolio/assets/"""
        # Créer un actif pour l'utilisateur
        Asset.objects.create(
            user=self.user,
            asset_type='STOCK',
            symbol='AAPL',
            name='Apple',
            quantity=Decimal('10.0'),
            purchase_price=Decimal('100.00'),
            current_price=Decimal('120.00'),
            purchase_date=date(2024, 1, 1)
        )
        
        response = self.client.get('/api/portfolio/assets/')
        
        assert response.status_code == status.HTTP_200_OK
        # Vérifier la structure de pagination
        assert 'results' in response.json() or 'count' in response.json()
    
    def test_get_portfolio_performance(self):
        """Test GET /api/portfolio/performance/"""
        response = self.client.get('/api/portfolio/performance/')
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert 'weighted_performance' in data
        assert 'assets' in data
    
    def test_unauthenticated_access(self):
        """Test accès non authentifié"""
        self.client.logout()
        response = self.client.get('/api/portfolio/summary/')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED