from typing import Dict, List
from decimal import Decimal
from django.core.exceptions import PermissionDenied

from .interfaces import IAssetRepository, IPerformanceCalculator
from .calculators import PortfolioMetricsCalculator


class PortfolioService:
    """Portfolio Service following Single Responsibility Principle"""
    
    def __init__(
        self,
        asset_repository: IAssetRepository,
        calculator: IPerformanceCalculator
    ):
        """Dependency Injection constructor"""
        self.asset_repository = asset_repository
        self.calculator = calculator
    
    def get_portfolio_summary(self, user_id: int) -> Dict:
        """Get portfolio summary"""
        assets = self.asset_repository.find_all_by_user(user_id)
        
        if not assets:
            return self._empty_summary()
        
        total_value = PortfolioMetricsCalculator.calculate_total_value(assets)
        total_investment = PortfolioMetricsCalculator.calculate_total_investment(assets)
        total_gain_loss = total_value - total_investment
        
        if total_investment > 0:
            total_performance = float((total_gain_loss / total_investment) * 100)
        else:
            total_performance = 0.0
        
        distribution = PortfolioMetricsCalculator.calculate_distribution(assets)
        
        return {
            'total_value': float(total_value),
            'total_investment': float(total_investment),
            'total_gain_loss': float(total_gain_loss),
            'total_performance': total_performance,
            'distribution': distribution,
            'asset_count': len(assets)
        }
    
    def get_portfolio_performance(self, user_id: int) -> Dict:
        """Get detailed portfolio performance"""
        assets = self.asset_repository.find_all_by_user(user_id)
        
        if not assets:
            return {
                'weighted_performance': 0,
                'assets': [],
                'total_value': 0
            }
        
        total_value = PortfolioMetricsCalculator.calculate_total_value(assets)
        weighted_performance = 0.0
        detailed_assets = []
        
        for asset in assets:
            asset_performance = self.calculator.calculate(asset)
            current_value = asset.current_value
            
            detailed_assets.append({
                'id': asset.id,
                'symbol': asset.symbol,
                'name': asset.name,
                'asset_type': asset.get_asset_type_display(),
                'quantity': float(asset.quantity),
                'purchase_price': float(asset.purchase_price),
                'current_price': float(asset.current_price),
                'current_value': float(current_value),
                'purchase_value': float(asset.purchase_value),
                'gain_loss': float(asset.gain_loss),
                'performance': asset_performance,
                'purchase_date': asset.purchase_date.isoformat(),
                'created_at': asset.created_at.isoformat()
            })
            
            if total_value > 0:
                weighted_performance += asset_performance * (float(current_value) / float(total_value))
        
        return {
            'weighted_performance': weighted_performance,
            'assets': detailed_assets,
            'total_value': float(total_value)
        }
    
    def get_asset_detail(self, asset_id: int, user_id: int) -> Dict:
        """Get asset detail with performance calculation"""
        asset = self.asset_repository.find_by_id(asset_id)
        
        if not asset or asset.user.id != user_id:
            raise PermissionDenied("Asset not found or access denied")
        
        performance = self.calculator.calculate(asset)
        
        return {
            'id': asset.id,
            'asset_type': asset.asset_type,
            'symbol': asset.symbol,
            'name': asset.name,
            'quantity': float(asset.quantity),
            'purchase_price': float(asset.purchase_price),
            'current_price': float(asset.current_price),
            'purchase_date': asset.purchase_date.isoformat(),
            'current_value': float(asset.current_value),
            'purchase_value': float(asset.purchase_value),
            'gain_loss': float(asset.gain_loss),
            'performance_percentage': asset.performance_percentage,
            'calculated_performance': performance,
            'created_at': asset.created_at.isoformat(),
            'updated_at': asset.updated_at.isoformat()
        }
    
    def _empty_summary(self) -> Dict:
        """Return empty summary"""
        return {
            'total_value': 0,
            'total_investment': 0,
            'total_gain_loss': 0,
            'total_performance': 0,
            'distribution': {},
            'asset_count': 0
        }