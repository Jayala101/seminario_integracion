# invoices/views/detail.py
from rest_framework import viewsets, permissions
from invoices.models import InvoiceDetail
from invoices.serializers.detail import InvoiceDetailSerializer

class InvoiceDetailViewSet(viewsets.ModelViewSet):
    queryset = InvoiceDetail.objects.select_related('invoice','product').all()
    serializer_class = InvoiceDetailSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.is_staff:
            return qs
        return qs.filter(invoice__user=user)

    def perform_create(self, serializer):
        invoice = serializer.validated_data.get('invoice')
        if (not self.request.user.is_staff) and invoice.user != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('No puedes modificar facturas de otros usuarios')
        if invoice.status != invoice.DRAFT:
            from rest_framework.exceptions import ValidationError
            raise ValidationError('Solo puedes agregar detalles cuando la factura está en DRAFT')
        serializer.save()
