from django.urls import path
from .views import TransactionListView, transfer_funds, withdraw_funds

app_name = 'transactions'

urlpatterns = [
    path('', TransactionListView.as_view(), name='transaction-list'),
    path('transfer/', transfer_funds, name='transfer'),
    path('withdraw/', withdraw_funds, name='withdraw'),
] 