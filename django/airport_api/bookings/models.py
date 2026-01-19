from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from flights.models import Flight
from passengers.models import Passenger
import uuid


class Booking(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pendiente'),
        ('CONFIRMED', 'Confirmada'),
        ('PAID', 'Pagada'),
        ('CANCELLED', 'Cancelada'),
        ('COMPLETED', 'Completada'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('CREDIT_CARD', 'Tarjeta de Crédito'),
        ('DEBIT_CARD', 'Tarjeta de Débito'),
        ('TRANSFER', 'Transferencia'),
        ('CASH', 'Efectivo'),
    ]
    
    booking_code = models.CharField(
        max_length=10,
        unique=True,
        editable=False
    )
    
    passenger = models.ForeignKey(
        Passenger,
        on_delete=models.PROTECT,
        related_name='bookings'
    )
    flight = models.ForeignKey(
        Flight,
        on_delete=models.PROTECT,
        related_name='bookings'
    )
    
    booking_date = models.DateTimeField(auto_now_add=True)
    travel_class = models.CharField(
        max_length=20,
        choices=Flight.CLASS_CHOICES,
        default='ECONOMY'
    )
    seat_number = models.CharField(max_length=10, blank=True)
    
    checked_baggage = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )
    carry_on_baggage = models.IntegerField(
        default=1,
        validators=[MinValueValidator(0)]
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        blank=True
    )
    amount_paid = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0
    )
    
    special_requests = models.TextField(blank=True)
    meal_preference = models.CharField(max_length=50, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-booking_date']
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
        indexes = [
            models.Index(fields=['booking_code']),
            models.Index(fields=['status']),
            models.Index(fields=['-booking_date']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['passenger', 'flight'],
                condition=models.Q(status__in=['PENDING', 'CONFIRMED', 'PAID']),
                name='unique_active_booking_per_passenger_flight'
            )
        ]
    
    def __str__(self):
        return f"{self.booking_code} - {self.passenger.full_name}"
    
    def save(self, *args, **kwargs):
        if not self.booking_code:
            self.booking_code = self.generate_booking_code()
        super().save(*args, **kwargs)
    
    def generate_booking_code(self):
        return f"BK{uuid.uuid4().hex[:8].upper()}"
    
    def clean(self):
        if self.flight and self.passenger:
            existing = Booking.objects.filter(
                flight=self.flight,
                passenger=self.passenger,
                status__in=['PENDING', 'CONFIRMED', 'PAID']
            ).exclude(pk=self.pk)
            
            if existing.exists():
                raise ValidationError('El pasajero ya tiene una reserva en este vuelo')
            
            if self.flight.available_seats <= 0 and self.status in ['PENDING', 'CONFIRMED', 'PAID']:
                raise ValidationError('No hay asientos disponibles en este vuelo')
    
    @property
    def is_active(self):
        return self.status in ['PENDING', 'CONFIRMED', 'PAID']
    
    @property
    def total_amount(self):
        """Calcula el monto total basado en el precio del vuelo y la clase"""
        from decimal import Decimal
        base = self.flight.base_price
        # Multiplicadores por clase
        multipliers = {
            'ECONOMY': Decimal('1.0'),
            'PREMIUM_ECONOMY': Decimal('1.5'),
            'BUSINESS': Decimal('2.5'),
            'FIRST_CLASS': Decimal('4.0'),
        }
        multiplier = multipliers.get(self.travel_class, Decimal('1.0'))
        return base * multiplier
