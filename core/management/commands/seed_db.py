import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction, connection
from django.utils import timezone
from datetime import timedelta

from wallets.models import Wallet

User = get_user_model()

class Command(BaseCommand):
    help = 'Popula o banco de dados com dados iniciais para testes'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Iniciando a população do banco de dados...'))
        
        # Verificar se a tabela wallets_wallet existe
        table_exists = self._check_table_exists('wallets_wallet')
        
        if not table_exists:
            self.stdout.write(self.style.WARNING(
                'A tabela wallets_wallet não existe. Criando apenas usuários.'
            ))
            self._create_test_users()
        else:
            with transaction.atomic():
                self._create_test_users()
                self._ensure_wallets()
                self._add_funds_to_wallets()
        
        self.stdout.write(self.style.SUCCESS('Banco de dados populado com sucesso!'))
    
    def _check_table_exists(self, table_name):
        """Verifica se uma tabela existe no banco de dados"""
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = %s
                )
            """, [table_name])
            return cursor.fetchone()[0]
    
    def _create_test_users(self):
        """Cria usuários de teste"""
        # Dados para usuários de teste
        test_users = [
            {
                'username': 'joao',
                'email': 'joao@example.com',
                'password': 'senha@123',
                'first_name': 'João',
                'last_name': 'Silva',
                'is_verified': True
            },
            {
                'username': 'maria',
                'email': 'maria@example.com',
                'password': 'senha@123',
                'first_name': 'Maria',
                'last_name': 'Santos',
                'is_verified': True
            },
            {
                'username': 'pedro',
                'email': 'pedro@example.com',
                'password': 'senha@123',
                'first_name': 'Pedro',
                'last_name': 'Oliveira',
                'is_verified': True
            },
            {
                'username': 'ana',
                'email': 'ana@example.com',
                'password': 'senha@123',
                'first_name': 'Ana',
                'last_name': 'Costa',
                'is_verified': True
            },
            {
                'username': 'carlos',
                'email': 'carlos@example.com',
                'password': 'senha@123',
                'first_name': 'Carlos',
                'last_name': 'Rodrigues',
                'is_verified': True
            },
        ]
        
        # Criando usuários
        for user_data in test_users:
            user, created = User.objects.get_or_create(
                email=user_data['email'],
                defaults={
                    'username': user_data['username'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'is_verified': user_data['is_verified']
                }
            )
            
            if created:
                user.set_password(user_data['password'])
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Usuário criado: {user.email}'))
            else:
                self.stdout.write(f'Usuário já existe: {user.email}')
    
    def _ensure_wallets(self):
        """Garante que todos os usuários tenham carteiras"""
        if not self._check_table_exists('wallets_wallet'):
            self.stdout.write(self.style.WARNING(
                'A tabela wallets_wallet não existe. Ignorando criação de carteiras.'
            ))
            return

        # Importar o modelo Wallet apenas se a tabela existir
        from wallets.models import Wallet
        
        # Consulta direta para evitar o JOIN com wallets_wallet que pode não existir
        for user in User.objects.all():
            wallet, created = Wallet.objects.get_or_create(user=user)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Carteira criada para {user.email}'))
            else:
                self.stdout.write(f'Carteira já existe para {user.email}')
    
    def _add_funds_to_wallets(self):
        """Adiciona fundos às carteiras dos usuários"""
        if not self._check_table_exists('wallets_wallet'):
            self.stdout.write(self.style.WARNING(
                'A tabela wallets_wallet não existe. Ignorando adição de fundos.'
            ))
            return
            
        # Importar o modelo Wallet apenas se a tabela existir
        from wallets.models import Wallet
        
        wallets = Wallet.objects.all()
        
        for wallet in wallets:
            # Adiciona um valor aleatório entre R$ 100,00 e R$ 5.000,00
            amount = Decimal(random.randint(10000, 500000)) / 100
            wallet.balance = amount
            wallet.save()
            self.stdout.write(self.style.SUCCESS(
                f'Adicionado R$ {amount:.2f} à carteira de {wallet.user.email}'
            ))
    
    def _create_sample_transactions(self):
        """Cria transações de exemplo entre usuários"""
        if not self._check_table_exists('transactions_transaction'):
            self.stdout.write(self.style.WARNING(
                'A tabela transactions_transaction não existe. Ignorando criação de transações.'
            ))
            return
        
        # Importar o modelo Transaction apenas se a tabela existir
        from transactions.models import Transaction
        from django.contrib.auth import get_user_model
        from wallets.models import Wallet
        import random
        from decimal import Decimal
        from datetime import timedelta
        from django.utils import timezone
        
        User = get_user_model()
        
        # Obter todos os usuários com carteiras
        users = User.objects.filter(wallet__isnull=False)
        if users.count() < 2:
            self.stdout.write(self.style.WARNING('Não há usuários suficientes para criar transações.'))
            return
        
        # Criar transações aleatórias
        for _ in range(20):
            # Escolher remetente e destinatário
            sender = random.choice(users)
            recipients = [u for u in users if u != sender]
            recipient = random.choice(recipients)
            
            # Valor aleatório entre R$10 e R$100
            amount = Decimal(random.randint(1000, 10000)) / 100
            
            # Data aleatória nos últimos 30 dias
            days_ago = random.randint(0, 30)
            transaction_date = timezone.now() - timedelta(days=days_ago)
            
            # Criar a transação
            transaction = Transaction.objects.create(
                transaction_type=Transaction.TRANSFER,
                status=Transaction.COMPLETED,
                sender=sender,
                recipient=recipient,
                amount=amount,
                description=f'Transação de teste - {random.randint(1000, 9999)}',
                created_at=transaction_date
            )
            
            self.stdout.write(self.style.SUCCESS(f'Transação de exemplo criada: {transaction}')) 