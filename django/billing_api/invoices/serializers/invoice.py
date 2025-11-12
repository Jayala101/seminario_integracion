# invoices/serializers/invoice.py
from rest_framework import serializers
from invoices.models import Invoice, InvoiceDetail

class InvoiceSerializer(serializers.ModelSerializer):
    details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Invoice
        fields = ('id','number','customer_name','customer_email','status',
                  'subtotal','tax','total','created_at','updated_at','details')
        read_only_fields = ('id','number','subtotal','tax','total','created_at','updated_at','details')

    def get_details(self, obj):
        qs = InvoiceDetail.objects.filter(invoice=obj).select_related('product')
        from invoices.serializers.detail import InvoiceDetailSerializer
        return InvoiceDetailSerializer(qs, many=True).data

class InvoiceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ('customer_name','customer_email')
