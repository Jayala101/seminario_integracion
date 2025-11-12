# invoices/signals.py
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from invoices.models import InvoiceDetail
from invoices.services.totals import compute_detail, recompute_invoice

@receiver(pre_save, sender=InvoiceDetail)
def set_detail_totals(sender, instance: InvoiceDetail, **kwargs):
    if not instance.unit_price:
        instance.unit_price = instance.product.price
    ls, lt, lt_total = compute_detail(instance)
    instance.line_subtotal = ls
    instance.line_tax = lt
    instance.line_total = lt_total

@receiver(post_save, sender=InvoiceDetail)
def recompute_after_detail_save(sender, instance: InvoiceDetail, created, **kwargs):
    recompute_invoice(instance.invoice)

@receiver(post_delete, sender=InvoiceDetail)
def recompute_after_detail_delete(sender, instance: InvoiceDetail, **kwargs):
    recompute_invoice(instance.invoice)
