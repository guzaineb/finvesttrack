from typing import List, Optional
from decimal import Decimal
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from ..models import Asset
from .interfaces import IAsset, IAssetRepository


class DjangoAssetRepository(IAssetRepository):
    """Concrete implementation of Asset Repository"""
    
    def find_by_id(self, asset_id: int) -> Optional[Asset]:
        try:
            return Asset.objects.get(id=asset_id)
        except ObjectDoesNotExist:
            return None
    
    def find_all_by_user(self, user_id: int) -> List[Asset]:
        return list(Asset.objects.filter(user_id=user_id))
    
    @transaction.atomic
    def save(self, asset: Asset) -> Asset:
        asset.save()
        return asset
    
    @transaction.atomic
    def delete(self, asset_id: int) -> bool:
        try:
            Asset.objects.filter(id=asset_id).delete()
            return True
        except Exception:
            return False
    