# invoices/views/invoice.py
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django.utils.crypto import get_random_string

from invoices.models import Invoice
from invoices.serializers.invoice import InvoiceSerializer, InvoiceCreateSerializer
from invoices.serializers.detail import InvoiceDetailSerializer
from invoices.services.totals import recompute_invoice
from catalog.models import Product

class IsOwnerOrStaff(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.user_id == request.user.id

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    filterset_fields = ('status',)
    search_fields = ('customer_name','customer_email','number')
    ordering_fields = ('created_at','total')

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user)
        return qs

    def get_serializer_class(self):
        if self.action in ('create','update','partial_update'):
            return InvoiceCreateSerializer
        return InvoiceSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def add_item(self, request, pk=None):
        """Agrega un detalle a la factura (solo si está en DRAFT)."""
        invoice = self.get_object()
        self.check_object_permissions(request, invoice)
        if invoice.status != Invoice.DRAFT:
            return Response({'detail':'Solo puedes agregar items en DRAFT'}, status=400)

        ser = InvoiceDetailSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save(invoice=invoice)
        recompute_invoice(invoice)
        return Response(InvoiceSerializer(invoice).data)

    @action(detail=True, methods=['post'])
    @transaction.atomic
    def finalize(self, request, pk=None):
        """Finaliza la factura: asigna número y descuenta stock."""
        invoice = self.get_object()
        self.check_object_permissions(request, invoice)
        if invoice.status != Invoice.DRAFT:
            return Response({'detail':'La factura no está en DRAFT'}, status=400)

        # Asignar número (simple: INV-XXXX)
        if not invoice.number:
            invoice.number = f'INV-{get_random_string(6).upper()}'

        # Validar stock
        for d in invoice.details.select_related('product'):
            p: Product = d.product
            if p.stock < d.quantity:
                return Response({'detail': f'Sin stock para {p.name}'}, status=400)

        # Descontar stock
        for d in invoice.details.select_related('product'):
            p: Product = d.product
            p.stock = p.stock - d.quantity
            p.save(update_fields=['stock'])

        invoice.status = Invoice.FINALIZED
        invoice.save(update_fields=['number','status'])
        recompute_invoice(invoice)
        return Response(InvoiceSerializer(invoice).data, status=200)

    @action(detail=True, methods=['post'])
    @transaction.atomic
    def cancel(self, request, pk=None):
        """Cancela la factura; si estaba FINALIZED, repone stock."""
        invoice = self.get_object()
        self.check_object_permissions(request, invoice)
        if invoice.status == Invoice.CANCELED:
            return Response({'detail':'La factura ya está cancelada'}, status=400)

        if invoice.status == Invoice.FINALIZED:
            for d in invoice.details.select_related('product'):
                p: Product = d.product
                p.stock = p.stock + d.quantity
                p.save(update_fields=['stock'])

        invoice.status = Invoice.CANCELED
        invoice.save(update_fields=['status'])
        recompute_invoice(invoice)
        return Response(InvoiceSerializer(invoice).data, status=200)
