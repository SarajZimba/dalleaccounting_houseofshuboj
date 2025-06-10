from django.urls import path
from receipt.views import ReceiptListView, ReceiptDetailView

urlpatterns = [
    path('receipts/', ReceiptListView.as_view(), name='receipt_list'),
    path('receipts/<int:pk>/', ReceiptDetailView.as_view(), name='receipt_card'),
]
