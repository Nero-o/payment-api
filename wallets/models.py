from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.utils.translation import gettext_lazy as _

class Wallet(models.Model):
    """Modelo para carteira digital dos usuários"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='wallet',
        verbose_name=_('usuário')
    )
    balance = models.DecimalField(
        _('saldo'),
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    is_active = models.BooleanField(_('ativa'), default=True)
    created_at = models.DateTimeField(_('criado em'), auto_now_add=True)
    updated_at = models.DateTimeField(_('atualizado em'), auto_now=True)
    
    class Meta:
        verbose_name = _('carteira')
        verbose_name_plural = _('carteiras')
        
    def __str__(self):
        return f"Carteira de {self.user.get_full_name() or self.user.username}" 