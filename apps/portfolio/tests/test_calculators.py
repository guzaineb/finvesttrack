import pytest
from datetime import date, timedelta
from decimal import Decimal
from django.contrib.auth import get_user_model
from apps.portfolio.models import Asset
from apps.portfolio.services.calculators import SimpleROICalculator, AnnualizedROICalculator

User = get_user_model()


@pytest.mark.django_db
class TestSimpleROICalculator:
    """Tests pour SimpleROICalculator"""

    def setup_method(self):
        """Setup avant chaque test"""
        self.user = User.objects.create_user(
            email='calculator@example.com',
            password='password123'
        )
        self.calculator = SimpleROICalculator()

    def test_calculate_positive_performance(self):
        """Test calcul ROI simple positif"""
        asset = Asset.objects.create(
            user=self.user,
            asset_type='STOCK',
            symbol='AAPL',
            name='Apple Inc.',
            quantity=Decimal('10.0'),
            purchase_price=Decimal('100.00'),
            current_price=Decimal('120.00'),  # Performance: +20%
            purchase_date=date.today() - timedelta(days=365)
        )

        result = self.calculator.calculate(asset)
        assert result == 20.0

    def test_calculate_negative_performance(self):
        """Test calcul ROI simple négatif"""
        asset = Asset.objects.create(
            user=self.user,
            asset_type='STOCK',
            symbol='TSLA',
            name='Tesla',
            quantity=Decimal('5.0'),
            purchase_price=Decimal('200.00'),
            current_price=Decimal('180.00'),  # Performance: -10%
            purchase_date=date.today() - timedelta(days=365)
        )

        result = self.calculator.calculate(asset)
        assert result == -10.0

    def test_calculate_zero_performance(self):
        """Test calcul ROI simple nul"""
        asset = Asset.objects.create(
            user=self.user,
            asset_type='STOCK',
            symbol='GOOGL',
            name='Google',
            quantity=Decimal('1.0'),
            purchase_price=Decimal('100.00'),
            current_price=Decimal('100.00'),  # Performance: 0%
            purchase_date=date.today() - timedelta(days=365)
        )

        result = self.calculator.calculate(asset)
        assert result == 0.0


@pytest.mark.django_db
class TestAnnualizedROICalculator:
    """Tests pour AnnualizedROICalculator"""

    def setup_method(self):
        """Setup avant chaque test"""
        self.user = User.objects.create_user(
            email='annualized@example.com',
            password='password123'
        )
        self.calculator = AnnualizedROICalculator()

    def test_calculate_one_year_positive(self):
        """Test calcul ROI annualisé sur 1 an positif"""
        asset = Asset.objects.create(
            user=self.user,
            asset_type='STOCK',
            symbol='AAPL',
            name='Apple Inc.',
            quantity=Decimal('10.0'),
            purchase_price=Decimal('100.00'),
            current_price=Decimal('120.00'),  # Performance: +20%
            purchase_date=date.today() - timedelta(days=365)
        )

        result = self.calculator.calculate(asset)
        # Pour 1 an, annualized ≈ simple ROI
        assert result == pytest.approx(20.0, abs=0.1)

    def test_calculate_six_months_positive(self):
        """Test calcul ROI annualisé sur 6 mois positif"""
        asset = Asset.objects.create(
            user=self.user,
            asset_type='STOCK',
            symbol='TSLA',
            name='Tesla',
            quantity=Decimal('5.0'),
            purchase_price=Decimal('200.00'),
            current_price=Decimal('220.00'),  # Performance: +10%
            purchase_date=date.today() - timedelta(days=182)  # ~6 mois
        )

        result = self.calculator.calculate(asset)
        # Annualisé devrait être plus élevé que 10%
        assert result > 10.0

    def test_calculate_negative_performance(self):
        """Test calcul ROI annualisé négatif"""
        asset = Asset.objects.create(
            user=self.user,
            asset_type='STOCK',
            symbol='NFLX',
            name='Netflix',
            quantity=Decimal('2.0'),
            purchase_price=Decimal('300.00'),
            current_price=Decimal('270.00'),  # Performance: -10%
            purchase_date=date.today() - timedelta(days=365)
        )

        result = self.calculator.calculate(asset)
        assert result == pytest.approx(-10.0, abs=0.1)

    def test_calculate_same_day(self):
        """Test calcul ROI annualisé même jour (edge case)"""
        asset = Asset.objects.create(
            user=self.user,
            asset_type='CRYPTO',
            symbol='BTC',
            name='Bitcoin',
            quantity=Decimal('0.1'),
            purchase_price=Decimal('50000.00'),
            current_price=Decimal('51000.00'),  # Performance: +2%
            purchase_date=date.today()
        )

        result = self.calculator.calculate(asset)
        # Avec days_held=1, annualized très élevé
        assert result > 700  # Approximation pour 2% en 1 jour

    def test_calculate_zero_purchase_value(self):
        """Test avec valeur d'achat nulle (edge case)"""
        asset = Asset.objects.create(
            user=self.user,
            asset_type='BOND',
            symbol='BOND1',
            name='Bond',
            quantity=Decimal('0.0'),  # Valeur achat = 0
            purchase_price=Decimal('100.00'),
            current_price=Decimal('100.00'),
            purchase_date=date.today() - timedelta(days=365)
        )

        result = self.calculator.calculate(asset)
        assert result == 0.0  # Devrait gérer la division par zéro
