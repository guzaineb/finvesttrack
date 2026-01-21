from .interfaces import IPerformanceCalculator, IAsset
from datetime import date


class SimpleROICalculator(IPerformanceCalculator):
    def calculate(self, asset: IAsset) -> float:
        """Calculate simple ROI percentage"""
        return float(asset.performance_percentage)


class AnnualizedROICalculator(IPerformanceCalculator):
    def calculate(self, asset: IAsset) -> float:
        """Calculate annualized ROI"""
        try:
            days_held = (date.today() - asset.purchase_date).days
        except:
            days_held = 1
        
        days_held = max(days_held, 1)  # Avoid division by zero
        
        total_return = 1 + (asset.performance_percentage / 100)
        annualized_return = (total_return ** (365 / days_held) - 1) * 100
        
        return annualized_return