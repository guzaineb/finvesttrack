import pytest
from datetime import date
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from apps.portfolio.services.asset_factory import AssetFactory

User = get_user_model()


@pytest.mark.django_db
class TestAssetFactory:
    """Tests pour le pattern Factory"""
    
    def setup_method(self):
        """Setup avant chaque test"""
        self.user = User.objects.create_user(
            email='factory@example.com',
            password='password123'
        )
    
    def test_create_stock(self):
        """Test création d'une action"""
        data = {
            'user': self.user,
            'symbol': 'AAPL',
            'name': 'Apple Inc.',
            'quantity': Decimal('10.0'),
            'purchase_price': Decimal('150.50'),
            'current_price': Decimal('175.25'),
            'purchase_date': date(2024, 1, 15)
        }
        
        asset = AssetFactory.create_asset('STOCK', **data)
        
        assert asset.asset_type == 'STOCK'
        assert asset.symbol == 'AAPL'
        assert asset.user == self.user
    
    def test_create_bond(self):
        """Test création d'une obligation"""
        data = {
            'user': self.user,
            'symbol': 'BOND1',
            'name': 'Government Bond',
            'quantity': Decimal('1000.0'),
            'purchase_price': Decimal('100.00'),
            'current_price': Decimal('102.50'),
            'purchase_date': date(2024, 1, 1)
        }
        
        asset = AssetFactory.create_asset('BOND', **data)
        
        assert asset.asset_type == 'BOND'
        assert asset.symbol == 'BOND1'
    
    def test_create_crypto(self):
        """Test création d'une crypto"""
        data = {
            'user': self.user,
            'symbol': 'BTC',
            'name': 'Bitcoin',
            'quantity': Decimal('0.5'),
            'purchase_price': Decimal('50000.00'),
            'current_price': Decimal('55000.00'),
            'purchase_date': date(2024, 1, 1)
        }
        
        asset = AssetFactory.create_asset('CRYPTO', **data)
        
        assert asset.asset_type == 'CRYPTO'
        assert asset.symbol == 'BTC'
    
    def test_create_invalid_asset_type(self):
        """Test type d'actif invalide"""
        data = {
            'user': self.user,
            'symbol': 'TEST',
            'name': 'Test',
            'quantity': Decimal('1.0'),
            'purchase_price': Decimal('100.00'),
            'current_price': Decimal('110.00'),
            'purchase_date': date(2024, 1, 1)
        }
        
        with pytest.raises(ValidationError, match="Type d'actif non supporté"):
            AssetFactory.create_asset('INVALID_TYPE', **data)
    
    def test_create_missing_required_field(self):
        """Test champ requis manquant"""
        data = {
            'user': self.user,
            'symbol': 'TEST',
            # 'name' manquant
            'quantity': Decimal('1.0'),
            'purchase_price': Decimal('100.00'),
            'current_price': Decimal('110.00'),
            'purchase_date': date(2024, 1, 1)
        }
        
        with pytest.raises(ValidationError, match="Champ manquant"):
            AssetFactory.create_asset('STOCK', **data)