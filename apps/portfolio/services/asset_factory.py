from django.core.exceptions import ValidationError
from ..models import Asset


class AssetFactory:
    """Factory Pattern for creating different types of assets"""
    _creators = {}
    
    @classmethod
    def register(cls, asset_type: str, creator):
        """Register a creator for an asset type"""
        cls._creators[asset_type] = creator
    
    @classmethod
    def create(cls, asset_type: str, **kwargs) -> Asset:
        """Create an asset of specified type"""
        if asset_type not in cls._creators:
            raise ValidationError(f"Type d'actif non supporté: {asset_type}")
        
        creator = cls._creators[asset_type]
        return creator(**kwargs)
    
    @classmethod
    def create_asset(cls, asset_type: str, **kwargs) -> Asset:
        """Create an asset with validation of required fields"""
        required_fields = [
            'symbol', 'name', 'quantity', 'purchase_price',
            'current_price', 'purchase_date', 'user'
        ]
        
        for field in required_fields:
            if field not in kwargs:
                raise ValidationError(f"Champ manquant: {field}")
        
        return cls.create(asset_type, **kwargs)


# Concrete creators
def create_stock(**kwargs) -> Asset:
    """Create a STOCK asset"""
    return Asset(asset_type='STOCK', **kwargs)


def create_bond(**kwargs) -> Asset:
    """Create a BOND asset"""
    return Asset(asset_type='BOND', **kwargs)


def create_crypto(**kwargs) -> Asset:
    """Create a CRYPTO asset"""
    return Asset(asset_type='CRYPTO', **kwargs)


# Register creators
AssetFactory.register('STOCK', create_stock)
AssetFactory.register('BOND', create_bond)
AssetFactory.register('CRYPTO', create_crypto)