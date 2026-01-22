from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import Asset
from .serializers import AssetSerializer
from .services.repositories import DjangoAssetRepository
from .services.calculators import SimpleROICalculator, AnnualizedROICalculator
from .services.portfolio_service import PortfolioService


class AssetViewSet(viewsets.ModelViewSet):
    """Gestion des actifs - Sans filtres complexes"""
    serializer_class = AssetSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'put', 'delete', 'head', 'options'] 
    def get_queryset(self):
        """Retourne uniquement les actifs de l'utilisateur connecté"""
        return Asset.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Assigne l'utilisateur lors de la création"""
        serializer.save(user=self.request.user)
    
    def retrieve(self, request, *args, **kwargs):
        """Détail d'un actif avec calcul de performance"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        # Utiliser SimpleROICalculator pour le détail
        calculator = SimpleROICalculator()
        repository = DjangoAssetRepository()
        service = PortfolioService(repository, calculator)
        
        try:
            asset_detail = service.get_asset_detail(instance.id, request.user.id)
            return Response(asset_detail)
        except Exception as e:
            # En cas d'erreur, retourner les données de base
            return Response(serializer.data)


class PortfolioSummaryView(APIView):
    """Vue pour le résumé du portefeuille"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Retourne le résumé du portefeuille"""
        repository = DjangoAssetRepository()
        calculator = SimpleROICalculator()
        service = PortfolioService(repository, calculator)
        
        summary = service.get_portfolio_summary(request.user.id)
        return Response(summary)


class PortfolioPerformanceView(APIView):
    """Vue pour la performance du portefeuille"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Retourne la performance détaillée"""
        repository = DjangoAssetRepository()
        calculator = SimpleROICalculator()
        service = PortfolioService(repository, calculator)
        
        performance = service.get_portfolio_performance(request.user.id)
        return Response(performance)