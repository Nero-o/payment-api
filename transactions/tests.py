from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from wallets.models import Wallet
from .models import Transaction

User = get_user_model()

class TransactionAPITests(TestCase):
    def setUp(self):
        # Criar usuários
        self.user1 = User.objects.create_user(
            username='user1', 
            email='user1@example.com',
            password='testpassword',
            first_name='Usuário',
            last_name='Um'
        )
        
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='testpassword',
            first_name='Usuário',
            last_name='Dois'
        )
        
        # Criar carteiras
        self.wallet1 = Wallet.objects.create(user=self.user1, balance=Decimal('1000.00'))
        self.wallet2 = Wallet.objects.create(user=self.user2, balance=Decimal('500.00'))
        
        # Setup client
        self.client = APIClient()
        
    def test_transfer_funds_success(self):
        # Login
        self.client.force_authenticate(user=self.user1)
        
        # Dados da transferência
        data = {
            'recipient_email': 'user2@example.com',
            'amount': '200.00',
            'description': 'Teste de transferência'
        }
        
        # Executar a transferência
        response = self.client.post(reverse('transactions:transfer'), data)
        
        # Verificar resposta
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verificar saldos atualizados
        self.wallet1.refresh_from_db()
        self.wallet2.refresh_from_db()
        self.assertEqual(self.wallet1.balance, Decimal('800.00'))
        self.assertEqual(self.wallet2.balance, Decimal('700.00'))
        
        # Verificar se a transação foi criada
        transaction = Transaction.objects.latest('created_at')
        self.assertEqual(transaction.sender, self.user1)
        self.assertEqual(transaction.recipient, self.user2)
        self.assertEqual(transaction.amount, Decimal('200.00'))
        self.assertEqual(transaction.status, Transaction.COMPLETED)
    
    def test_transfer_insufficient_funds(self):
        # Login
        self.client.force_authenticate(user=self.user1)
        
        # Dados da transferência com valor maior que o saldo
        data = {
            'recipient_email': 'user2@example.com',
            'amount': '1200.00',
            'description': 'Teste de transferência com fundos insuficientes'
        }
        
        # Executar a transferência
        response = self.client.post(reverse('transactions:transfer'), data)
        
        # Verificar resposta de erro
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Saldo insuficiente', response.data['amount'][0])
        
        # Verificar que os saldos não foram alterados
        self.wallet1.refresh_from_db()
        self.wallet2.refresh_from_db()
        self.assertEqual(self.wallet1.balance, Decimal('1000.00'))
        self.assertEqual(self.wallet2.balance, Decimal('500.00'))
    
    def test_list_transactions(self):
        # Criar algumas transações
        Transaction.objects.create(
            transaction_type=Transaction.TRANSFER,
            status=Transaction.COMPLETED,
            sender=self.user1,
            recipient=self.user2,
            amount=Decimal('100.00'),
            description='Transação prévia 1'
        )
        
        Transaction.objects.create(
            transaction_type=Transaction.TRANSFER,
            status=Transaction.COMPLETED,
            sender=self.user2,
            recipient=self.user1,
            amount=Decimal('50.00'),
            description='Transação prévia 2'
        )
        
        # Login como user1
        self.client.force_authenticate(user=self.user1)
        
        # Listar transações
        response = self.client.get(reverse('transactions:transaction-list'))
        
        # Verificar resposta
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # Ambas as transações 