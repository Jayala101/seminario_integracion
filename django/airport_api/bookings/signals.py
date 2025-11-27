from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Booking


@receiver(post_save, sender=Booking)
def update_flight_on_booking_save(sender, instance, created, **kwargs):
    if created or instance.status in ['PENDING', 'CONFIRMED', 'PAID']:
        pass


@receiver(post_delete, sender=Booking)
def update_flight_on_booking_delete(sender, instance, **kwargs):
    pass
    pass
