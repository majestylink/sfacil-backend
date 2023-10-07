from django.urls import path

from transaction.views import TransactionView

urlpatterns = [
    path('', TransactionView.as_view(), name='transaction_view'),
    path('<str:transaction_id>/', TransactionView.as_view(), name='transaction_detail'),
]
