from django.urls import path
from .views import WalletDetailView, deposit_funds

app_name = 'wallets'

urlpatterns = [
    path('', WalletDetailView.as_view(), name='wallet-detail'),
    path('deposit/', deposit_funds, name='deposit'),
]