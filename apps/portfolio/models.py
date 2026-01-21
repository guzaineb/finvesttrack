from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Asset(models.Model):
    class AssetType(models.TextChoices):
        STOCK = 'STOCK', 'Action'
        BOND = 'BOND', 'Obligation'
        CRYPTO = 'CRYPTO', 'Crypto-monnaie'
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assets')
    asset_type = models.CharField(max_length=10, choices=AssetType.choices)
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=18, decimal_places=8)
    purchase_price = models.DecimalField(max_digits=18, decimal_places=2)
    current_price = models.DecimalField(max_digits=18, decimal_places=2)
    purchase_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def current_value(self):
        return self.quantity * self.current_price
    
    @property
    def performance_percentage(self):
        purchase_value = self.quantity * self.purchase_price
        if purchase_value == 0:
            return 0
        return ((self.current_value - purchase_value) / purchase_value) * 100
    
    @property
    def gain_loss(self):
        return self.current_value - (self.quantity * self.purchase_price)
    
    def __str__(self):
        return f"{self.symbol} - {self.asset_type}"