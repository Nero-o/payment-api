from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.utils.translation import gettext_lazy as _

class Transaction(models.Model):
    """Modelo para transações financeiras entre carteiras"""
    # Tipos de transação
    DEPOSIT = 'deposit'
    TRANSFER = 'transfer'
    WITHDRAWAL = 'withdrawal'
    
    TRANSACTION_TYPES = [
        (DEPOSIT, _('Depósito')),
        (TRANSFER, _('Transferência')),
        (WITHDRAWAL, _('Saque')),
    ]
    
    # Status da transação
    PENDING = 'pending'
    COMPLETED = 'completed'
    FAILED = 'failed'
    
    TRANSACTION_STATUS = [
        (PENDING, _('Pendente')),
        (COMPLETED, _('Concluída')),
        (FAILED, _('Falha')),
    ]
    
    # Campos de transação
    transaction_type = models.CharField(
        _('tipo'),
        max_length=10,
        choices=TRANSACTION_TYPES
    )
    
    status = models.CharField(
        _('status'),
        max_length=10,
        choices=TRANSACTION_STATUS,
        default=PENDING
    )
    
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='sent_transactions',
        null=True,  # Para depósitos, o sender pode ser null
        blank=True,
        verbose_name=_('remetente')
    )
    
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='received_transactions',
        null=True,  # Para saques, o recipient pode ser null
        blank=True,
        verbose_name=_('destinatário')
    )
    
    amount = models.DecimalField(
        _('valor'),
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    
    description = models.CharField(
        _('descrição'),
        max_length=255,
        blank=True
    )
    
    created_at = models.DateTimeField(
        _('data de criação'),
        auto_now_add=True
    )
    
    updated_at = models.DateTimeField(
        _('data de atualização'),
        auto_now=True
    )
    
    class Meta:
        verbose_name = _('transação')
        verbose_name_plural = _('transações')
        ordering = ['-created_at']
    
    def __str__(self):
        if self.transaction_type == self.DEPOSIT:
            return f"Depósito de R${self.amount} para {self.recipient}"
        elif self.transaction_type == self.WITHDRAWAL:
            return f"Saque de R${self.amount} por {self.sender}"
        else:
            return f"Transferência de R${self.amount} de {self.sender} para {self.recipient}" 