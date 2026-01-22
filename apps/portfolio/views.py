from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from .models import Asset
from .serializers import AssetSerializer
from .services.repositories import DjangoAssetRepository
from .services.calculators import SimpleROICalculator, AnnualizedROICalculator
from .services.portfolio_service import PortfolioService


class AssetViewSet(viewsets.ModelViewSet):
    """Asset ViewSet with CRUD operations"""
    serializer_class = AssetSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['asset_type']
    search_fields = ['symbol', 'name']
    ordering_fields = ['created_at', 'current_value', 'performance_percentage']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Return only user's assets"""
        return Asset.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Set user on asset creation"""
        serializer.save(user=self.request.user)
    
    def perform_update(self, serializer):
        """Prevent user change on update"""
        serializer.save()
    
    @action(detail=True, methods=['put'])
    def update_price(self, request, pk=None):
        """Update asset current price"""
        asset = self.get_object()
        new_price = request.data.get('current_price')
        
        if not new_price:
            return Response(
                {'error': 'current_price est requis.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            asset.update_current_price(new_price)
            return Response(self.get_serializer(asset).data)
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class PortfolioSummaryView(generics.GenericAPIView):
    """Portfolio summary view"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get portfolio summary"""
        service = PortfolioService(
            asset_repository=DjangoAssetRepository(),
            calculator=SimpleROICalculator()
        )
        
        summary = service.get_portfolio_summary(request.user.id)
        return Response(summary)


class PortfolioPerformanceView(generics.GenericAPIView):
    """Portfolio performance view"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get portfolio performance"""
        calculator_type = request.query_params.get('calculator', 'simple')
        
        if calculator_type == 'annualized':
            calculator = AnnualizedROICalculator()
        else:
            calculator = SimpleROICalculator()
        
        service = PortfolioService(
            asset_repository=DjangoAssetRepository(),
            calculator=calculator
        )
        
        performance = service.get_portfolio_performance(request.user.id)
        return Response(performance)


class AssetDetailView(generics.GenericAPIView):
    """Asset detail view with performance"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, asset_id):
        """Get asset detail with performance"""
        calculator_type = request.query_params.get('calculator', 'simple')
        
        if calculator_type == 'annualized':
            calculator = AnnualizedROICalculator()
        else:
            calculator = SimpleROICalculator()
        
        service = PortfolioService(
            asset_repository=DjangoAssetRepository(),
            calculator=calculator
        )
        
        try:
            asset_detail = service.get_asset_detail(asset_id, request.user.id)
            return Response(asset_detail)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_404_NOT_FOUND
            )