from rest_framework import serializers
from django.contrib.auth import get_user_model
from decimal import Decimal

from .models import Transaction
from wallets.models import Wallet

User = get_user_model()

class UserBasicSerializer(serializers.ModelSerializer):
    """Serializer simplificado para informações básicas do usuário"""
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name']
        
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}" if obj.first_name else obj.username

class TransactionSerializer(serializers.ModelSerializer):
    """Serializer para exibição de transações"""
    sender = UserBasicSerializer(read_only=True)
    recipient = UserBasicSerializer(read_only=True)
    transaction_type_display = serializers.CharField(source='get_transaction_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Transaction
        fields = [
            'id', 'transaction_type', 'transaction_type_display', 
            'status', 'status_display', 'sender', 'recipient',
            'amount', 'description', 'created_at', 'updated_at'
        ]
        read_only_fields = fields

class TransferSerializer(serializers.Serializer):
    """Serializer para transferências entre usuários"""
    recipient_email = serializers.EmailField(write_only=True)
    amount = serializers.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        min_value=Decimal('0.01')
    )
    description = serializers.CharField(
        max_length=255, 
        required=False, 
        allow_blank=True
    )
    
    def validate_recipient_email(self, value):
        try:
            recipient = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Usuário destinatário não encontrado.")
        
        sender = self.context['request'].user
        if recipient.id == sender.id:
            raise serializers.ValidationError("Você não pode transferir para si mesmo.")
        
        return value
        
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("O valor da transferência deve ser maior que zero.")
        
        sender = self.context['request'].user
        try:
            sender_wallet = Wallet.objects.get(user=sender)
            if sender_wallet.balance < value:
                raise serializers.ValidationError("Saldo insuficiente para esta transferência.")
        except Wallet.DoesNotExist:
            raise serializers.ValidationError("Você não possui uma carteira ativa.")
            
        return value 

class WithdrawalSerializer(serializers.Serializer):
    """Serializer para saques"""
    amount = serializers.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        min_value=Decimal('0.01')
    )
    description = serializers.CharField(
        max_length=255, 
        required=False, 
        allow_blank=True
    )
    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("O valor do saque deve ser maior que zero.")
        
        user = self.context['request'].user
        try:
            wallet = Wallet.objects.get(user=user)
            if wallet.balance < value:
                raise serializers.ValidationError("Saldo insuficiente para este saque.")
        except Wallet.DoesNotExist:
            raise serializers.ValidationError("Você não possui uma carteira ativa.")
            
        return value 