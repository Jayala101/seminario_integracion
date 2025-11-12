# invoices/models/invoice.py
from django.db import models
from django.contrib.auth.models import User

class Invoice(models.Model):
    DRAFT = 'DRAFT'
    FINALIZED = 'FINALIZED'
    CANCELED = 'CANCELED'
    STATUS_CHOICES = [
        (DRAFT, 'Borrador'),
        (FINALIZED, 'Finalizada'),
        (CANCELED, 'Cancelada'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invoices')
    number = models.CharField(max_length=32, unique=True, blank=True)  # asignado al finalizar
    customer_name = models.CharField(max_length=160)
    customer_email = models.EmailField(blank=True)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=DRAFT)

    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'Invoice #{self.id} - {self.customer_name}'
