from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Asset
from .serializers import AssetSerializer
from .services.portfolio_service import PortfolioService
from .services.calculators import SimpleROICalculator

from rest_framework.permissions import IsAuthenticated

class PortfolioSummaryView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]  # ← Ceci utilise JWT Authentication
    
    def get(self, request):
        # request.user est automatiquement défini par JWT
        service = PortfolioService(calculator=SimpleROICalculator())
        summary = service.get_portfolio_summary(request.user.id)  # ← request.user.id
        return Response(summary)
class AssetViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des actifs"""
    serializer_class = AssetSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['asset_type']
    
    # Ajouter queryset pour éviter l'erreur
    queryset = Asset.objects.all()
    
    def get_queryset(self):
        """Retourne uniquement les actifs de l'utilisateur connecté"""
        return self.queryset.filter(user=self.request.user).order_by('-created_at')
    
    def perform_create(self, serializer):
        """Assigne automatiquement l'utilisateur à l'actif créé"""
        serializer.save(user=self.request.user)


class PortfolioPerformanceView(generics.GenericAPIView):
    """Vue pour la performance du portefeuille"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Retourne la performance détaillée"""
        service = PortfolioService(calculator=SimpleROICalculator())
        performance = service.get_portfolio_performance(request.user.id)
        return Response(performance)