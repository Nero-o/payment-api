from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """
    Modelo de usuário personalizado para o sistema de carteira digital.
    Estende o modelo de usuário padrão do Django com campos adicionais.
    """
    email = models.EmailField(
        _('endereço de email'),
        unique=True,
        error_messages={
            'unique': _('Um usuário com este email já existe.'),
        }
    )
    
    phone_number = models.CharField(
        _('número de telefone'), 
        max_length=15, 
        blank=True, 
        null=True
    )
    
    is_verified = models.BooleanField(
        _('verificado'),
        default=False,
        help_text=_('Indica se o usuário verificou seu email/telefone.')
    )
    
    # Campos de auditoria
    created_at = models.DateTimeField(_('criado em'), auto_now_add=True)
    updated_at = models.DateTimeField(_('atualizado em'), auto_now=True)
    
    # Configura o email como campo de login
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        verbose_name = _('usuário')
        verbose_name_plural = _('usuários')
        
    def __str__(self):
        return self.email
    
    @property
    def full_name(self):
        """Retorna o nome completo do usuário"""
        return f"{self.first_name} {self.last_name}"