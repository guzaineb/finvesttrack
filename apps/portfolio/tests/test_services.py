from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from datetime import date
from apps.portfolio.models import Asset
from apps.portfolio.services.repositories import DjangoAssetRepository
from apps.portfolio.services.calculators import SimpleROICalculator
from apps.portfolio.services.portfolio_service import PortfolioService

User = get_user_model()


class TestPortfolioService(TestCase):
    """Tests du service PortfolioService"""

    def setUp(self):
        self.user = User.objects.create_user(
            email="portfolio@test.com",
            username="portfolio",
            password="password123"
        )

        Asset.objects.create(
            user=self.user,
            asset_type="STOCK",
            symbol="AAPL",
            name="Apple",
            quantity=Decimal("10"),
            purchase_price=Decimal("100"),
            current_price=Decimal("150"),
            purchase_date=date.today()
        )

        self.service = PortfolioService(
            DjangoAssetRepository(),
            SimpleROICalculator()
        )

    def test_portfolio_summary(self):
        summary = self.service.get_portfolio_summary(self.user.id)

        self.assertEqual(summary["asset_count"], 1)
        self.assertEqual(summary["total_value"], 1500.0)
        self.assertEqual(summary["total_gain_loss"], 500.0)

    def test_get_asset_detail(self):
        asset = Asset.objects.first()
        detail = self.service.get_asset_detail(asset.id, self.user.id)

        self.assertEqual(detail["symbol"], "AAPL")
        self.assertEqual(detail["performance_percentage"], 50.0)
