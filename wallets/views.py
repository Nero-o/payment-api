from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.db import transaction
from .models import Wallet
from .serializers import WalletSerializer, DepositSerializer

class WalletDetailView(generics.RetrieveAPIView):
    """Endpoint para visualizar detalhes da carteira do usuário logado"""
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        # Obtém ou cria a carteira para o usuário logado
        wallet, created = Wallet.objects.get_or_create(user=self.request.user)
        return wallet

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deposit_funds(request):
    """Endpoint para adicionar fundos à carteira do usuário"""
    serializer = DepositSerializer(data=request.data)
    if serializer.is_valid():
        amount = serializer.validated_data['amount']
        
        # Obter ou criar a carteira
        wallet, created = Wallet.objects.get_or_create(user=request.user)
        
        # Adicionar o valor à carteira usando uma transação atômica
        with transaction.atomic():
            wallet.balance += amount
            wallet.save()
        
        return Response({
            "message": f"Depósito de R$ {amount} realizado com sucesso.",
            "wallet": WalletSerializer(wallet).data
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 