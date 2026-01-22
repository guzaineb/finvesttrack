from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import Asset
from .services.asset_factory import AssetFactory


class AssetSerializer(serializers.ModelSerializer):
    """Asset Serializer with calculated fields"""
    current_value = serializers.DecimalField(
        max_digits=18,
        decimal_places=2,
        read_only=True
    )
    gain_loss = serializers.DecimalField(
        max_digits=18,
        decimal_places=2,
        read_only=True
    )
    performance_percentage = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    
    class Meta:
        model = Asset
        fields = [
            'id',
            'asset_type',
            'symbol',
            'name',
            'quantity',
            'purchase_price',
            'current_price',
            'purchase_date',
            'current_value',
            'gain_loss',
            'performance_percentage',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']
    
    def validate(self, data):
        """Validate asset data"""
        # Validate quantity
        if data.get('quantity', 0) <= 0:
            raise ValidationError({"quantity": "La quantité doit être positive."})
        
        # Validate prices
        if data.get('purchase_price', 0) <= 0:
            raise ValidationError({"purchase_price": "Le prix d'achat doit être positif."})
        
        if data.get('current_price', 0) < 0:
            raise ValidationError({"current_price": "Le prix courant ne peut pas être négatif."})
        
        return data
    
    def create(self, validated_data):
        """Create asset using Factory Pattern"""
        request = self.context.get('request')
        
        if not request or not request.user.is_authenticated:
            raise ValidationError("Utilisateur non authentifié.")
        
        asset_type = validated_data.pop('asset_type')
        validated_data['user'] = request.user
        
        try:
            asset = AssetFactory.create_asset(asset_type, **validated_data)
            asset.save()
            return asset
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)
    
    def update(self, instance, validated_data):
        """Update asset - prevent changing asset_type and user"""
        if 'asset_type' in validated_data and validated_data['asset_type'] != instance.asset_type:
            raise ValidationError({"asset_type": "Le type d'actif ne peut pas être modifié."})
        
        if 'user' in validated_data:
            validated_data.pop('user')
        
        return super().update(instance, validated_data)