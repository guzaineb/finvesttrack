import pytest
from datetime import date
from decimal import Decimal
from django.contrib.auth import get_user_model
from apps.portfolio.models import Asset

User = get_user_model()


@pytest.mark.django_db
class TestAssetModel:
    """Tests unitaires pour le modèle Asset"""
    
    def test_create_asset(self):
        """Test création d'un actif"""
        user = User.objects.create_user(
            email='test@example.com',
            password='password123'
        )
        
        asset = Asset.objects.create(
            user=user,
            asset_type='STOCK',
            symbol='AAPL',
            name='Apple Inc.',
            quantity=Decimal('10.0'),
            purchase_price=Decimal('150.50'),
            current_price=Decimal('175.25'),
            purchase_date=date(2024, 1, 15)
        )
        
        assert asset.symbol == 'AAPL'
        assert asset.asset_type == 'STOCK'
        assert asset.user == user
    
    def test_current_value_calculation(self):
        """Test du calcul de la valeur actuelle"""
        user = User.objects.create_user(email='test2@example.com', password='pass')
        
        asset = Asset.objects.create(
            user=user,
            asset_type='CRYPTO',
            symbol='BTC',
            name='Bitcoin',
            quantity=Decimal('0.5'),
            purchase_price=Decimal('50000.00'),
            current_price=Decimal('55000.00'),
            purchase_date=date(2024, 1, 1)
        )
        
        # 0.5 * 55000 = 27500
        expected_value = Decimal('27500.00')
        assert asset.current_value == expected_value
    
    def test_performance_percentage(self):
        """Test du calcul de performance"""
        user = User.objects.create_user(email='test3@example.com', password='pass')
        
        asset = Asset.objects.create(
            user=user,
            asset_type='BOND',
            symbol='BOND1',
            name='Government Bond',
            quantity=Decimal('100.0'),
            purchase_price=Decimal('100.00'),  # Achat à 100
            current_price=Decimal('110.00'),   # Actuel à 110
            purchase_date=date(2024, 1, 1)
        )
        
        # Gain de 10% : ((110-100)/100)*100 = 10%
        assert asset.performance_percentage == 10.0
    
    def test_zero_performance(self):
        """Test performance à 0%"""
        user = User.objects.create_user(email='test4@example.com', password='pass')
        
        asset = Asset.objects.create(
            user=user,
            asset_type='STOCK',
            symbol='TEST',
            name='Test',
            quantity=Decimal('10.0'),
            purchase_price=Decimal('100.00'),
            current_price=Decimal('100.00'),  # Même prix
            purchase_date=date(2024, 1, 1)
        )
        
        assert asset.performance_percentage == 0.0