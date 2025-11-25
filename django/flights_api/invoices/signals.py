from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from decimal import Decimal
from .models import Booking, BookingDetail
import random
import string


def generate_booking_number():
    """Genera un número de reserva único"""
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=8))


@receiver(post_save, sender=Booking)
def set_booking_number(sender, instance, created, **kwargs):
    """Asigna un número de reserva cuando se crea"""
    if created and not instance.booking_number:
        instance.booking_number = generate_booking_number()
        instance.save(update_fields=['booking_number'])


@receiver(post_save, sender=BookingDetail)
@receiver(post_delete, sender=BookingDetail)
def update_booking_totals(sender, instance, **kwargs):
    """Actualiza los totales de la reserva cuando se agregan/eliminan detalles"""
    booking = instance.booking
    passengers = booking.passengers.all()
    
    # Calcular subtotal
    subtotal = sum(p.total_price for p in passengers)
    
    # Calcular impuestos (16%)
    tax = subtotal * Decimal('0.16')
    
    # Tarifa de servicio ($10 por pasajero)
    service_fee = passengers.count() * Decimal('10.00')
    
    # Total
    total = subtotal + tax + service_fee
    
    booking.subtotal = subtotal
    booking.tax = tax
    booking.service_fee = service_fee
    booking.total = total
    booking.save(update_fields=['subtotal', 'tax', 'service_fee', 'total'])


@receiver(post_save, sender=Booking)
def set_confirmed_date(sender, instance, created, **kwargs):
    """Establece la fecha de confirmación cuando el estado cambia a CONFIRMED"""
    if not created and instance.status == 'CONFIRMED' and not instance.confirmed_at:
        instance.confirmed_at = timezone.now()
        instance.save(update_fields=['confirmed_at'])
