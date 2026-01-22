from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from decimal import Decimal
from django.contrib.auth import get_user_model

User = get_user_model()


class IAsset(ABC):
    """Asset Interface following Interface Segregation Principle"""
    
    @property
    @abstractmethod
    def id(self) -> int:
        pass
    
    @property
    @abstractmethod
    def symbol(self) -> str:
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        pass
    
    @property
    @abstractmethod
    def asset_type(self) -> str:
        pass
    
    @property
    @abstractmethod
    def quantity(self) -> Decimal:
        pass
    
    @property
    @abstractmethod
    def purchase_price(self) -> Decimal:
        pass
    
    @property
    @abstractmethod
    def current_price(self) -> Decimal:
        pass
    
    @property
    @abstractmethod
    def purchase_date(self):
        pass
    
    @property
    @abstractmethod
    def current_value(self) -> Decimal:
        pass
    
    @property
    @abstractmethod
    def purchase_value(self) -> Decimal:
        pass
    
    @property
    @abstractmethod
    def gain_loss(self) -> Decimal:
        pass
    
    @property
    @abstractmethod
    def performance_percentage(self) -> float:
        pass


class IPerformanceCalculator(ABC):
    """Performance Calculator Interface"""
    
    @abstractmethod
    def calculate(self, asset: IAsset) -> float:
        pass


class IAssetRepository(ABC):
    """Asset Repository Interface following Dependency Inversion Principle"""
    
    @abstractmethod
    def find_by_id(self, asset_id: int) -> Optional[IAsset]:
        pass
    
    @abstractmethod
    def find_all_by_user(self, user_id: int) -> List[IAsset]:
        pass
    
    @abstractmethod
    def save(self, asset: IAsset) -> IAsset:
        pass
    
    @abstractmethod
    def delete(self, asset_id: int) -> bool:
        pass
    