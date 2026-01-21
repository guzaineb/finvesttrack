from django.core.exceptions import ValidationError
from ..models import Asset


class AssetFactory:
    """Factory Pattern pour créer différents types d'actifs"""
    _creators = {}
    
    @classmethod
    def register(cls, asset_type: str, creator):
        cls._creators[asset_type] = creator
    
    @classmethod
    def create(cls, asset_type: str, **kwargs):
        """Crée un actif du type spécifié"""
        if asset_type not in cls._creators:
            raise ValidationError(f"Type d'actif non supporté: {asset_type}")
        
        creator = cls._creators[asset_type]
        # Le créateur s'occupe de mettre le bon asset_type
        return creator(**kwargs)
    
    @classmethod
    def create_asset(cls, asset_type: str, **kwargs):
        """Crée un actif avec validation des champs requis"""
        required = ['symbol', 'name', 'quantity', 'purchase_price', 
                   'current_price', 'purchase_date', 'user']
        
        for field in required:
            if field not in kwargs:
                raise ValidationError(f"Champ manquant: {field}")
        
        # NE PAS ajouter asset_type aux kwargs
        return cls.create(asset_type, **kwargs)


# Fonctions de création SIMPLIFIÉES
def create_stock(**kwargs):
    """Crée un actif de type STOCK"""
    return Asset(asset_type='STOCK', **kwargs)


def create_bond(**kwargs):
    """Crée un actif de type BOND"""
    return Asset(asset_type='BOND', **kwargs)


def create_crypto(**kwargs):
    """Crée un actif de type CRYPTO"""
    return Asset(asset_type='CRYPTO', **kwargs)


# Enregistrement
AssetFactory.register('STOCK', create_stock)
AssetFactory.register('BOND', create_bond)
AssetFactory.register('CRYPTO', create_crypto)