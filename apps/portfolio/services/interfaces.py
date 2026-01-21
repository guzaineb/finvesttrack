from abc import ABC, abstractmethod
from typing import Dict, List
from decimal import Decimal


class IAsset(ABC):
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
    def current_value(self) -> Decimal:
        pass
    
    @property
    @abstractmethod
    def gain_loss(self) -> Decimal:
        pass
    
    @property
    @abstractmethod
    def performance_percentage(self) -> float:
        pass
    
    @property
    @abstractmethod
    def purchase_date(self):
        pass


class IPerformanceCalculator(ABC):
    @abstractmethod
    def calculate(self, asset: IAsset) -> float:
        pass