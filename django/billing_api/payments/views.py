# payments/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from invoices.models.invoice import Invoice
from .repositories import ensure_indexes, create_payment_plan, add_payment_transaction, get_plan_with_transactions

class InitMongoIndexesView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        ensure_indexes()
        return Response({"ok": True})

class PaymentPlanCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        invoice_id = request.data.get("invoice_id")
        customer_id = request.data.get("customer_id")
        total = request.data.get("total")
        installments = request.data.get("installments", 1)
        currency = request.data.get("currency", "USD")

        if invoice_id is None or customer_id is None or total is None:
            return Response({"detail": "invoice_id, customer_id y total son requeridos"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            invoice_id = int(invoice_id)
            customer_id = int(customer_id)
            total = float(total)
            installments = int(installments)
        except Exception:
            return Response({"detail": "Tipos inválidos en invoice_id/customer_id/total/installments"}, status=status.HTTP_400_BAD_REQUEST)

        if not Invoice.objects.filter(id=invoice_id).exists():
            return Response({"detail": "La factura no existe"}, status=status.HTTP_404_NOT_FOUND)

        doc = create_payment_plan(invoice_id, customer_id, total, installments, currency)
        return Response({
            "plan_id": str(doc["_id"]),
            "invoice_id": doc["invoice_id"],
            "status": doc["status"]
        }, status=status.HTTP_201_CREATED)

class PaymentTransactionCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        plan_id = request.data.get("plan_id")
        invoice_id = request.data.get("invoice_id")
        amount = request.data.get("amount")
        method = request.data.get("method")
        reference = request.data.get("reference", "")
        meta = request.data.get("meta", {})

        if not plan_id or invoice_id is None or amount is None or not method:
            return Response({"detail": "plan_id, invoice_id, amount y method son requeridos"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            invoice_id = int(invoice_id)
            amount = float(amount)
        except Exception:
            return Response({"detail": "invoice_id o amount inválidos"}, status=status.HTTP_400_BAD_REQUEST)

        if not Invoice.objects.filter(id=invoice_id).exists():
            return Response({"detail": "La factura no existe"}, status=status.HTTP_404_NOT_FOUND)

        try:
            doc = add_payment_transaction(plan_id, invoice_id, amount, method, reference, meta)
        except Exception:
            return Response({"detail": "plan_id inválido o reference duplicada"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "transaction_id": str(doc["_id"]),
            "plan_id": str(doc["plan_id"]),
            "invoice_id": doc["invoice_id"],
            "amount": doc["amount"],
            "method": doc["method"],
            "paid_at": doc["paid_at"].isoformat(),
        }, status=status.HTTP_201_CREATED)

class InvoicePaymentsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, invoice_id: int):
        if not Invoice.objects.filter(id=invoice_id).exists():
            return Response({"detail": "La factura no existe"}, status=status.HTTP_404_NOT_FOUND)

        data = get_plan_with_transactions(invoice_id)
        if not data:
            return Response({"detail": "No hay plan de pagos para esta factura"}, status=status.HTTP_404_NOT_FOUND)

        return Response(data, status=status.HTTP_200_OK)