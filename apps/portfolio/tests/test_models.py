import pytest
from datetime import date
from decimal import Decimal
from django.contrib.auth import get_user_model
from apps.portfolio.models import Asset

User = get_user_model()


@pytest.mark.django_db
class TestAssetModel:
    """Tests pour le modèle Asset"""
    
    def setup_method(self):
        """Setup avant chaque test"""
        self.user = User.objects.create_user(
            email='assetowner@example.com',
            password='password123'
        )
    
    def test_create_asset(self):
        """Test création d'un actif"""
        asset = Asset.objects.create(
            user=self.user,
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
        assert asset.user == self.user
        assert asset.current_value == Decimal('1752.50')  # 10 * 175.25
    
    def test_current_value_calculation(self):
        """Test calcul de la valeur actuelle"""
        asset = Asset.objects.create(
            user=self.user,
            asset_type='CRYPTO',
            symbol='BTC',
            name='Bitcoin',
            quantity=Decimal('0.5'),
            purchase_price=Decimal('50000.00'),
            current_price=Decimal('55000.00'),
            purchase_date=date(2024, 1, 1)
        )
        
        # 0.5 * 55000 = 27500
        assert asset.current_value == Decimal('27500.00')
    
    def test_gain_loss_positive(self):
        """Test gain positif"""
        asset = Asset.objects.create(
            user=self.user,
            asset_type='STOCK',
            symbol='GAIN',
            name='Gain Stock',
            quantity=Decimal('100.0'),
            purchase_price=Decimal('1.00'),   # Achat à 1
            current_price=Decimal('1.50'),    # Actuel à 1.5
            purchase_date=date(2024, 1, 1)
        )
        
        # Gain de 50: (100 * 1.5) - (100 * 1) = 150 - 100 = 50
        assert asset.gain_loss == Decimal('50.00')
    
    def test_gain_loss_negative(self):
        """Test perte"""
        asset = Asset.objects.create(
            user=self.user,
            asset_type='BOND',
            symbol='LOSS',
            name='Loss Bond',
            quantity=Decimal('1000.0'),
            purchase_price=Decimal('100.00'),  # Achat à 100
            current_price=Decimal('95.00'),    # Actuel à 95
            purchase_date=date(2024, 1, 1)
        )
        
        # Perte de 5000: (1000 * 95) - (1000 * 100) = 95000 - 100000 = -5000
        assert asset.gain_loss == Decimal('-5000.00')
    
    def test_performance_percentage_positive(self):
        """Test performance positive"""
        asset = Asset.objects.create(
            user=self.user,
            asset_type='STOCK',
            symbol='POS',
            name='Positive',
            quantity=Decimal('10.0'),
            purchase_price=Decimal('100.00'),  # Achat à 100
            current_price=Decimal('120.00'),   # Actuel à 120 (+20%)
            purchase_date=date(2024, 1, 1)
        )
        
        # Performance: ((120-100)/100)*100 = 20%
        assert asset.performance_percentage == 20.0
    
