from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'transaction_type', 'status', 'sender', 'recipient', 'amount', 'created_at')
    list_filter = ('transaction_type', 'status', 'created_at')
    search_fields = ('sender__email', 'recipient__email', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (None, {
            'fields': ('transaction_type', 'status', 'sender', 'recipient', 'amount', 'description')
        }),
        ('Informações temporais', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('sender', 'recipient') 