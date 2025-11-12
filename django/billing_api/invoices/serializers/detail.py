# invoices/serializers/detail.py
from rest_framework import serializers
from invoices.models import InvoiceDetail
from catalog.models import Product

class InvoiceDetailSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        source='product', queryset=Product.objects.all(), write_only=True
    )
    product_name = serializers.ReadOnlyField(source='product.name')

    class Meta:
        model = InvoiceDetail
        fields = ('id','invoice','product_id','product_name','quantity','unit_price',
                  'line_subtotal','line_tax','line_total')
        read_only_fields = ('id','line_subtotal','line_tax','line_total','product_name')
