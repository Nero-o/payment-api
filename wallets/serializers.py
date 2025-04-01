from rest_framework import serializers
from .models import Wallet
from decimal import Decimal

class WalletSerializer(serializers.ModelSerializer):
    """Serializer para exibição da carteira"""
    user_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Wallet
        fields = ['id', 'user_name', 'balance', 'is_active', 'created_at', 'updated_at']
        read_only_fields = fields
        
    def get_user_name(self, obj):
        return obj.user.get_full_name() or obj.user.username

class DepositSerializer(serializers.Serializer):
    """Serializer para depósitos na carteira"""
    amount = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2,
        min_value=Decimal('0.01')
    )
    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("O valor do depósito deve ser maior que zero.")
        return value 