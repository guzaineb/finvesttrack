from rest_framework import serializers
from .models import Asset
from .services.asset_factory import AssetFactory


class AssetSerializer(serializers.ModelSerializer):
    current_value = serializers.DecimalField(max_digits=18, decimal_places=2, read_only=True)
    gain_loss = serializers.DecimalField(max_digits=18, decimal_places=2, read_only=True)
    performance_percentage = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Asset
        fields = [
            'id', 'asset_type', 'symbol', 'name', 'quantity',
            'purchase_price', 'current_price', 'purchase_date',
            'current_value', 'gain_loss', 'performance_percentage',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'user']
    
    def create(self, validated_data):
        """Create asset using factory pattern - VERSION CORRIGÉE"""
        request = self.context.get('request')
        
        # Extraction de asset_type
        asset_type = validated_data.pop('asset_type')  # ← Supprimez-le des kwargs
        
        # Ajouter l'utilisateur
        validated_data['user'] = request.user
        
        # Création via factory - N'AJOUTEZ PAS asset_type dans les kwargs
        # La factory va l'utiliser directement comme premier argument
        asset = AssetFactory.create_asset(asset_type, **validated_data)
        asset.save()
        return asset