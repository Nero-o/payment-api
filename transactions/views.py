from rest_framework import generics, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.db.models import Q
from django_filters import rest_framework as filters
from django.contrib.auth import get_user_model
from decimal import Decimal

from .models import Transaction
from .serializers import TransactionSerializer, TransferSerializer, WithdrawalSerializer
from wallets.models import Wallet

User = get_user_model()

class DateRangeFilter(filters.FilterSet):
    """Filtro para consulta de transações por período de data"""
    start_date = filters.DateTimeFilter(field_name="created_at", lookup_expr='gte')
    end_date = filters.DateTimeFilter(field_name="created_at", lookup_expr='lte')
    
    class Meta:
        model = Transaction
        fields = ['transaction_type', 'status', 'start_date', 'end_date']

class TransactionListView(generics.ListAPIView):
    """Endpoint para listar transações do usuário autenticado"""
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = DateRangeFilter
    ordering_fields = ['created_at', 'amount']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Retorna apenas transações do usuário autenticado"""
        user = self.request.user
        return Transaction.objects.filter(
            Q(sender=user) | Q(recipient=user)
        ).select_related('sender', 'recipient')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def transfer_funds(request):
    """Endpoint para transferência de fundos entre usuários"""
    serializer = TransferSerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        sender = request.user
        recipient_email = serializer.validated_data['recipient_email']
        amount = serializer.validated_data['amount']
        description = serializer.validated_data.get('description', '')
        
        try:
            recipient = User.objects.get(email=recipient_email)
            
            with transaction.atomic():
                # Verificar novamente se o saldo é suficiente (evitar race conditions)
                sender_wallet = Wallet.objects.select_for_update().get(user=sender)
                
                if sender_wallet.balance < amount:
                    return Response({
                        "error": "Saldo insuficiente para esta transferência."
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                # Obter ou criar a carteira do destinatário
                recipient_wallet, created = Wallet.objects.select_for_update().get_or_create(
                    user=recipient,
                    defaults={'balance': 0}
                )
                
                # Atualizar saldos
                sender_wallet.balance -= amount
                recipient_wallet.balance += amount
                
                sender_wallet.save()
                recipient_wallet.save()
                
                # Criar o registro da transação
                transaction_obj = Transaction.objects.create(
                    transaction_type=Transaction.TRANSFER,
                    status=Transaction.COMPLETED,
                    sender=sender,
                    recipient=recipient,
                    amount=amount,
                    description=description
                )
                
                return Response({
                    "message": f"Transferência de R$ {amount} realizada com sucesso.",
                    "transaction": TransactionSerializer(transaction_obj).data
                }, status=status.HTTP_201_CREATED)
                
        except User.DoesNotExist:
            return Response({
                "error": "Usuário destinatário não encontrado."
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "error": f"Erro ao processar a transferência: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def withdraw_funds(request):
    """Endpoint para realizar saque da carteira"""
    serializer = WithdrawalSerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        user = request.user
        amount = Decimal(serializer.validated_data['amount'])
        description = serializer.validated_data.get('description', '')
        
        try:
            with transaction.atomic():
                # Obter a carteira do usuário com bloqueio
                wallet = Wallet.objects.select_for_update().get(user=user)
                
                # Verificar se há saldo suficiente
                if wallet.balance < amount:
                    return Response({
                        "error": "Saldo insuficiente para realizar o saque."
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                # Atualizar o saldo
                wallet.balance -= amount
                wallet.save()
                
                # Criar o registro da transação
                transaction_obj = Transaction.objects.create(
                    transaction_type=Transaction.WITHDRAWAL,
                    status=Transaction.COMPLETED,
                    sender=user,
                    recipient=None,  # Saque não tem destinatário
                    amount=amount,
                    description=description
                )
                
                return Response({
                    "message": f"Saque de R$ {amount} realizado com sucesso.",
                    "transaction": TransactionSerializer(transaction_obj).data,
                    "new_balance": wallet.balance
                }, status=status.HTTP_201_CREATED)
                
        except Wallet.DoesNotExist:
            return Response({
                "error": "Carteira não encontrada."
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "error": f"Erro ao processar o saque: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 