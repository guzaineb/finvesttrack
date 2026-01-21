import pytest
from datetime import date
from decimal import Decimal
from django.contrib.auth import get_user_model
from apps.portfolio.models import Asset
from apps.portfolio.services.portfolio_service import PortfolioService
from apps.portfolio.services.calculators import SimpleROICalculator

User = get_user_model()


@pytest.mark.django_db
class TestPortfolioService:
    """Tests pour le service Portfolio"""
    
    def setup_method(self):
        """Setup avant chaque test"""
        self.user = User.objects.create_user(
            email='service@example.com',
            password='password123'
        )
        self.service = PortfolioService(calculator=SimpleROICalculator())
    
    def test_empty_portfolio_summary(self):
        """Test portfolio vide"""
        summary = self.service.get_portfolio_summary(self.user.id)
        
        assert summary['total_value'] == 0
        assert summary['total_gain_loss'] == 0
        assert summary['asset_count'] == 0
        assert summary['distribution'] == {}
    
    def test_portfolio_with_one_asset(self):
        """Test portfolio avec un actif"""
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
        
        summary = self.service.get_portfolio_summary(self.user.id)
        
        assert summary['total_value'] == 1200.0  # 10 * 120
        assert summary['total_gain_loss'] == 200.0  # 10 * (120-100)
        assert summary['asset_count'] == 1
        assert 'Action' in summary['distribution']
    
    def test_portfolio_with_multiple_assets(self):
        """Test portfolio avec plusieurs actifs"""
        # Créer 2 actifs
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
        
        Asset.objects.create(
            user=self.user,
            asset_type='CRYPTO',
            symbol='BTC',
            name='Bitcoin',
            quantity=Decimal('0.5'),
            purchase_price=Decimal('50000.00'),
            current_price=Decimal('55000.00'),
            purchase_date=date(2024, 1, 1)
        )
        
        summary = self.service.get_portfolio_summary(self.user.id)
        
        assert summary['asset_count'] == 2
        assert summary['total_value'] > 0
        # Vérifier la distribution
        assert len(summary['distribution']) == 2
        assert 'Action' in summary['distribution']
        assert 'Crypto-monnaie' in summary['distribution']


@pytest.mark.django_db
class TestCalculators:
    """Tests pour les calculateurs"""
    
    def test_simple_roi_calculator(self):
        """Test du calculateur ROI simple"""
        user = User.objects.create_user(email='calc@example.com', password='pass')
        
        asset = Asset.objects.create(
            user=user,
            asset_type='STOCK',
            symbol='TEST',
            name='Test',
            quantity=Decimal('100.0'),
            purchase_price=Decimal('1.00'),
            current_price=Decimal('1.50'),
            purchase_date=date(2024, 1, 1)
        )
        
        calculator = SimpleROICalculator()
        result = calculator.calculate(asset)
        
        # 50% de gain
        assert result == 50.0