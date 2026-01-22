import pytest
from datetime import date
from decimal import Decimal
from django.contrib.auth import get_user_model
from apps.portfolio.models import Asset
from apps.portfolio.services.portfolio_service import PortfolioService
from apps.portfolio.services.calculators import SimpleROICalculator

User = get_user_model()


@pytest.fixture
def portfolio_user():
    """Fixture pour l'utilisateur du portfolio"""
    return User.objects.create_user(
        email='portfolio@example.com',
        password='password123'
    )


@pytest.fixture
def portfolio_service():
    """Fixture pour le service"""
    return PortfolioService(calculator=SimpleROICalculator())


@pytest.fixture
def apple_stock(portfolio_user):
    """Fixture pour un actif Apple"""
    return Asset.objects.create(
        user=portfolio_user,
        asset_type='STOCK',
        symbol='AAPL',
        name='Apple Inc.',
        quantity=Decimal('10.0'),
        purchase_price=Decimal('100.00'),  # Valeur achat: 1000
        current_price=Decimal('120.00'),   # Valeur actuelle: 1200 (+20%)
        purchase_date=date(2024, 1, 1)
    )


@pytest.fixture  
def bitcoin_crypto(portfolio_user):
    """Fixture pour Bitcoin"""
    return Asset.objects.create(
        user=portfolio_user,
        asset_type='CRYPTO',
        symbol='BTC',
        name='Bitcoin',
        quantity=Decimal('1.0'),
        purchase_price=Decimal('1000.00'),  # Valeur achat: 1000
        current_price=Decimal('1100.00'),   # Valeur actuelle: 1100 (+10%)
        purchase_date=date(2024, 1, 1)
    )


@pytest.mark.django_db
class TestPortfolioService:
    """Tests optimisés pour le service Portfolio"""
    
    def test_empty_portfolio_summary(self, portfolio_user, portfolio_service):
        """Test portfolio vide"""
        summary = portfolio_service.get_portfolio_summary(portfolio_user.id)
        
        assert summary['total_value'] == 0
        assert summary['total_investment'] == 0
        assert summary['total_gain_loss'] == 0
        assert summary['total_performance'] == 0
        assert summary['distribution'] == {}
        assert summary['asset_count'] == 0
    
    def test_portfolio_with_one_asset(self, portfolio_user, portfolio_service, apple_stock):
        """Test portfolio avec un actif"""
        summary = portfolio_service.get_portfolio_summary(portfolio_user.id)
        
        # Tests principaux (sans refaire les calculs)
        assert summary['asset_count'] == 1
        assert summary['total_value'] > 0
        assert summary['total_investment'] > 0
        assert summary['total_gain_loss'] > 0
        assert summary['total_performance'] > 0
        
        # Vérifier la cohérence des données
        assert summary['total_gain_loss'] == summary['total_value'] - summary['total_investment']
        if summary['total_investment'] > 0:
            expected_perf = (summary['total_gain_loss'] / summary['total_investment']) * 100
            assert summary['total_performance'] == pytest.approx(expected_perf, 0.1)
        
        # Vérifier la distribution
        assert 'Action' in summary['distribution']
        assert summary['distribution']['Action'] == pytest.approx(100.0, 0.1)
    
    def test_portfolio_distribution_multiple_types(self, portfolio_user, portfolio_service, 
                                                  apple_stock, bitcoin_crypto):
        """Test la distribution avec plusieurs types d'actifs"""
        summary = portfolio_service.get_portfolio_summary(portfolio_user.id)
        
        assert summary['asset_count'] == 2
        assert len(summary['distribution']) == 2
        
        # Vérifier que la distribution somme à 100%
        total_percent = sum(summary['distribution'].values())
        assert total_percent == pytest.approx(100.0, 0.1)
    
    def test_portfolio_performance_empty(self, portfolio_user, portfolio_service):
        """Test performance portfolio vide"""
        performance = portfolio_service.get_portfolio_performance(portfolio_user.id)
        
        assert performance['weighted_performance'] == 0
        assert performance['assets'] == []
        assert performance['total_value'] == 0
    
    def test_portfolio_performance_structure(self, portfolio_user, portfolio_service, 
                                            apple_stock, bitcoin_crypto):
        """Test la structure des données de performance"""
        performance = portfolio_service.get_portfolio_performance(portfolio_user.id)
        
        assert performance['total_value'] > 0
        assert len(performance['assets']) == 2
        
        # Vérifier la structure de chaque actif
        for asset_data in performance['assets']:
            required_fields = ['id', 'symbol', 'name', 'asset_type', 'quantity', 
                             'purchase_price', 'current_price', 'current_value',
                             'purchase_value', 'gain_loss', 'performance', 'purchase_date']
            
            for field in required_fields:
                assert field in asset_data
            
            # Vérifier la cohérence des calculs
            assert asset_data['current_value'] == asset_data['quantity'] * asset_data['current_price']
            assert asset_data['purchase_value'] == asset_data['quantity'] * asset_data['purchase_price']
            assert asset_data['gain_loss'] == asset_data['current_value'] - asset_data['purchase_value']
    
    def test_portfolio_weighted_performance(self, portfolio_user, portfolio_service,
                                           apple_stock, bitcoin_crypto):
        """Test le calcul de performance pondérée"""
        performance = portfolio_service.get_portfolio_performance(portfolio_user.id)
        
        # Calcul manuel pour vérification
        assets_data = performance['assets']
        total_value = performance['total_value']
        
        calculated_weighted = 0.0
        for asset in assets_data:
            weight = asset['current_value'] / total_value
            calculated_weighted += asset['performance'] * weight
        
        assert performance['weighted_performance'] == pytest.approx(calculated_weighted, 0.1)
    
    def test_asset_isolation(self, portfolio_user, portfolio_service):
        """Test que chaque utilisateur voit seulement ses propres actifs"""
        # Créer un deuxième utilisateur
        user2 = User.objects.create_user(
            email='other@example.com',
            password='password456'
        )
        
        # Ajouter un actif au deuxième utilisateur
        Asset.objects.create(
            user=user2,
            asset_type='STOCK',
            symbol='GOOGL',
            name='Google',
            quantity=Decimal('5.0'),
            purchase_price=Decimal('200.00'),
            current_price=Decimal('210.00'),
            purchase_date=date(2024, 1, 1)
        )
        
        # Premier utilisateur (vide)
        summary1 = portfolio_service.get_portfolio_summary(portfolio_user.id)
        assert summary1['asset_count'] == 0
        
        # Deuxième utilisateur (1 actif)
        summary2 = portfolio_service.get_portfolio_summary(user2.id)
        assert summary2['asset_count'] == 1