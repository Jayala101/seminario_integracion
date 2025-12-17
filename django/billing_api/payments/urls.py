# payments/urls.py
from django.urls import path
from .views import (
    InitMongoIndexesView,
    PaymentPlanCreateView,
    PaymentTransactionCreateView,
    InvoicePaymentsView,
)

urlpatterns = [
    path("mongo/indexes/", InitMongoIndexesView.as_view()),
    path("payment-plans/", PaymentPlanCreateView.as_view()),
    path("payment-transactions/", PaymentTransactionCreateView.as_view()),
    path("invoices/<int:invoice_id>/payments/", InvoicePaymentsView.as_view()),
]