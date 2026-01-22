from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from datetime import date
from django.core.exceptions import ValidationError
from apps.portfolio.services.asset_factory import AssetFactory

User = get_user_model()


class TestAssetFactory(TestCase):
    """Tests du Factory Pattern pour Asset"""

    def setUp(self):
        self.user = User.objects.create_user(
            email="factory@test.com",
            username="factory",
            password="password123"
        )

    def test_create_stock_asset_success(self):
        asset = AssetFactory.create_asset(
            asset_type="STOCK",
            symbol="AAPL",
            name="Apple",
            quantity=Decimal("5"),
            purchase_price=Decimal("100"),
            current_price=Decimal("120"),
            purchase_date=date.today(),
            user=self.user
        )

        self.assertEqual(asset.asset_type, "STOCK")
        self.assertEqual(asset.symbol, "AAPL")

    def test_invalid_asset_type(self):
        with self.assertRaises(ValidationError):
            AssetFactory.create_asset(asset_type="INVALID")
