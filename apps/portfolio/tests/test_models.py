from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from datetime import date
from apps.portfolio.models import Asset

User = get_user_model()


class TestAssetModel(TestCase):
    """Tests du modèle Asset"""

    def setUp(self):
        self.user = User.objects.create_user(
            email="user@test.com",
            username="user",
            password="password123"
        )

    def test_asset_calculated_fields(self):
        asset = Asset.objects.create(
            user=self.user,
            asset_type="STOCK",
            symbol="AAPL",
            name="Apple",
            quantity=Decimal("10"),
            purchase_price=Decimal("100"),
            current_price=Decimal("150"),
            purchase_date=date.today()
        )

        self.assertEqual(asset.purchase_value, Decimal("1000"))
        self.assertEqual(asset.current_value, Decimal("1500"))
        self.assertEqual(asset.gain_loss, Decimal("500"))
        self.assertEqual(asset.performance_percentage, 50.0)
