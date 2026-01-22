from django.db import models
from django.contrib.auth import get_user_model
from decimal import Decimal

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
    def current_value(self) -> Decimal:
        """Valeur actuelle = quantité × prix courant"""
        try:
            return self.quantity * self.current_price
        except:
            return Decimal('0')
    
    @property
    def purchase_value(self) -> Decimal:
        """Valeur d'achat = quantité × prix d'achat"""
        try:
            return self.quantity * self.purchase_price
        except:
            return Decimal('0')
    
    @property
    def gain_loss(self) -> Decimal:
        """Gain/Perte = valeur actuelle - valeur d'achat"""
        try:
            return self.current_value - self.purchase_value
        except:
            return Decimal('0')
    
    @property
    def performance_percentage(self) -> float:
        """Performance en pourcentage = (gain/perte ÷ valeur d'achat) × 100"""
        try:
            if self.purchase_value == 0:
                return 0.0
            return float((self.gain_loss / self.purchase_value) * 100)
        except:
            return 0.0
    
    @property
    def performance_display(self) -> str:
        """Formatage de la performance pour l'affichage"""
        perf = self.performance_percentage
        return f"{'+' if perf >= 0 else ''}{perf:.2f}%"
    
    def update_current_price(self, new_price: Decimal):
        """Mettre à jour le prix courant et sauvegarder"""
        self.current_price = new_price
        self.save(update_fields=['current_price', 'updated_at'])
    
    def __str__(self):
        return f"{self.symbol} ({self.get_asset_type_display()}) - {self.performance_display}"