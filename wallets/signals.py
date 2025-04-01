from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.db import connection
from .models import Wallet

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_wallet_for_new_user(sender, instance, created, **kwargs):
    """Cria uma carteira para cada novo usuário"""
    if created:
        # Verifica se a tabela wallets_wallet existe antes de tentar criar
        try:
            # Verifica se a tabela existe
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name='wallets_wallet')"
                )
                table_exists = cursor.fetchone()[0]
                
            if table_exists:
                Wallet.objects.create(user=instance)
        except Exception as e:
            # Durante migrações iniciais, ignorar erros silenciosamente
            pass 