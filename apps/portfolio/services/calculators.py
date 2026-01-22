from datetime import date
from decimal import Decimal
from typing import Dict
from .interfaces import IAsset, IPerformanceCalculator


class SimpleROICalculator(IPerformanceCalculator):
    """Simple ROI Calculator Strategy"""
    
    def calculate(self, asset: IAsset) -> float:
        """Calculate simple Return on Investment percentage"""
        try:
            return float(asset.performance_percentage)
        except (TypeError, ValueError):
            return 0.0


class AnnualizedROICalculator(IPerformanceCalculator):
    """Annualized ROI Calculator Strategy"""
    
    def calculate(self, asset: IAsset) -> float:
        """Calculate annualized Return on Investment"""
        try:
            days_held = (date.today() - asset.purchase_date).days
            days_held = max(days_held, 1)  # Avoid division by zero
            
            total_return = 1 + (asset.performance_percentage / 100)
            annualized_return = (total_return ** (365 / days_held) - 1) * 100
            
            return float(annualized_return)
        except (TypeError, ValueError, ZeroDivisionError):
            return 0.0


class PortfolioMetricsCalculator:
    """Portfolio metrics calculator following Single Responsibility Principle"""
    
    @staticmethod
    def calculate_total_value(assets: list) -> Decimal:
        """Calculate total portfolio value"""
        return sum((asset.current_value for asset in assets), Decimal('0'))
    
    @staticmethod
    def calculate_total_investment(assets: list) -> Decimal:
        """Calculate total portfolio investment"""
        return sum((asset.purchase_value for asset in assets), Decimal('0'))
    
    @staticmethod
    def calculate_distribution(assets: list) -> Dict[str, float]:
        """Calculate asset type distribution"""
        distribution = {}
        total_value = PortfolioMetricsCalculator.calculate_total_value(assets)
        
        if total_value == 0:
            return {}
        
        for asset in assets:
            asset_type = asset.get_asset_type_display()
            distribution[asset_type] = distribution.get(asset_type, Decimal('0')) + asset.current_value
        
        return {
            asset_type: float((value / total_value) * 100)
            for asset_type, value in distribution.items()
        }