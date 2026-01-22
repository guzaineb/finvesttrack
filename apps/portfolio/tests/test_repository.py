import pytest
from decimal import Decimal
from datetime import date
from django.contrib.auth import get_user_model
from apps.portfolio.models import Asset
from apps.portfolio.services.repositories import DjangoAssetRepository

User = get_user_model()

@pytest.mark.django_db
def test_repository_find_all_by_user():
    user = User.objects.create_user(
        username="repo",
        email="repo@test.com",
        password="1234"
    )

    Asset.objects.create(
        user=user,
        asset_type="CRYPTO",
        symbol="BTC",
        name="Bitcoin",
        quantity=Decimal("1"),
        purchase_price=Decimal("20000"),
        current_price=Decimal("30000"),
        purchase_date=date.today()
    )

    repo = DjangoAssetRepository()
    assets = repo.find_all_by_user(user.id)

    assert len(assets) == 1
