from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from apps.portfolio.models import Asset

User = get_user_model()


class TestAssetAPI(TestCase):
    """Tests des endpoints Assets"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="api@test.com",
            username="api",
            password="password123"
        )

    def test_create_asset_authenticated(self):
        self.client.force_authenticate(user=self.user)

        url = reverse("asset-list")

        response = self.client.post(url, {
            "asset_type": "STOCK",
            "symbol": "AAPL",
            "name": "Apple",
            "quantity": 10,
            "purchase_price": 100,
            "current_price": 150,
            "purchase_date": "2024-01-01"
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Asset.objects.count(), 1)

    def test_create_asset_unauthenticated(self):
        url = reverse("asset-list")

        response = self.client.post(url, {
            "asset_type": "STOCK",
            "symbol": "AAPL",
            "name": "Apple",
            "quantity": 10,
            "purchase_price": 100,
            "current_price": 150,
            "purchase_date": "2024-01-01"
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
