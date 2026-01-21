from typing import Dict, List
from decimal import Decimal
from django.db.models import Sum
from ..models import Asset
from .interfaces import IPerformanceCalculator


class PortfolioService:
    def __init__(self, calculator: IPerformanceCalculator):
        self.calculator = calculator
    
    def get_portfolio_summary(self, user_id: int) -> Dict:
        """Get portfolio summary with distribution by type"""
        assets = Asset.objects.filter(user_id=user_id)
        
        if not assets.exists():
            return self._empty_summary()
        
        total_value = assets.aggregate(total=Sum('current_value'))['total'] or Decimal('0')
        total_gain_loss = sum(asset.gain_loss for asset in assets)
        
        distribution = {}
        for asset in assets:
            asset_type = asset.get_asset_type_display()
            distribution[asset_type] = distribution.get(asset_type, 0) + float(asset.current_value)
        
        # Calculate percentages
        if total_value > 0:
            distribution = {k: (v / float(total_value)) * 100 for k, v in distribution.items()}
        
        total_performance = self._calculate_total_performance(assets, total_gain_loss, total_value)
        
        return {
            'total_value': float(total_value),
            'total_gain_loss': float(total_gain_loss),
            'total_performance': total_performance,
            'distribution': distribution,
            'asset_count': assets.count()
        }
    
    def get_portfolio_performance(self, user_id: int) -> Dict:
        """Get detailed performance for each asset"""
        assets = Asset.objects.filter(user_id=user_id)
        
        performances = []
        total_value = Decimal('0')
        
        for asset in assets:
            performance = self.calculator.calculate(asset)
            current_value = asset.current_value
            total_value += current_value
            
            performances.append({
                'id': asset.id,
                'symbol': asset.symbol,
                'name': asset.name,
                'asset_type': asset.get_asset_type_display(),
                'performance': performance,
                'current_value': float(current_value)
            })
        
        # Calculate weighted average performance
        weighted_performance = 0
        if total_value > 0:
            for p in performances:
                weight = p['current_value'] / float(total_value)
                weighted_performance += p['performance'] * weight
        
        return {
            'weighted_performance': weighted_performance,
            'assets': performances,
            'total_value': float(total_value)
        }
    
    def _empty_summary(self) -> Dict:
        return {
            'total_value': 0,
            'total_gain_loss': 0,
            'total_performance': 0,
            'distribution': {},
            'asset_count': 0
        }
    
    def _calculate_total_performance(self, assets: List[Asset], total_gain_loss: Decimal, total_value: Decimal) -> float:
        """Calculate total portfolio performance percentage"""
        if total_value == 0:
            return 0.0
        
        total_investment = total_value - total_gain_loss
        if total_investment == 0:
            return 0.0
        
        return (float(total_gain_loss) / float(total_investment)) * 100