# invoices/services/totals.py
from decimal import Decimal, ROUND_HALF_UP
import os

TAX_RATE = Decimal(os.getenv('TAX_RATE', '0.12'))  # 12% por defecto

def quantize(amount):
    return amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

def compute_detail(detail):
    """
    Calcula los importes de una línea (subtotal, impuesto y total).
    No guarda el detalle; solo retorna los valores.
    """
    subtotal = Decimal(detail.unit_price) * detail.quantity
    tax = quantize(subtotal * TAX_RATE)
    total = quantize(subtotal + tax)
    return quantize(subtotal), tax, total

def recompute_invoice(invoice):
    """
    Recalcula subtotal, impuesto y total de la factura en base a sus details.
    """
    from invoices.models import InvoiceDetail  # import local para evitar ciclos
    details = InvoiceDetail.objects.filter(invoice=invoice)
    subtotal = sum((d.line_subtotal for d in details), Decimal('0'))
    tax = sum((d.line_tax for d in details), Decimal('0'))
    total = sum((d.line_total for d in details), Decimal('0'))
    invoice.subtotal = quantize(Decimal(subtotal))
    invoice.tax = quantize(Decimal(tax))
    invoice.total = quantize(Decimal(total))
    invoice.save(update_fields=['subtotal','tax','total'])
