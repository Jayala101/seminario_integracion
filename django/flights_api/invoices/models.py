from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal


class Booking(models.Model):
    """Modelo para representar reservas de vuelos"""
    STATUS_CHOICES = [
        ('PENDING', 'Pendiente'),
        ('CONFIRMED', 'Confirmada'),
        ('CANCELLED', 'Cancelada'),
        ('COMPLETED', 'Completada'),
    ]
    
    # Información del usuario
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='bookings'
    )
    
    # Información de la reserva
    booking_number = models.CharField(
        max_length=32, 
        unique=True, 
        blank=True,
        help_text="Número de reserva generado automáticamente"
    )
    status = models.CharField(
        max_length=16, 
        choices=STATUS_CHOICES, 
        default='PENDING'
    )
    
    # Información del pasajero principal
    passenger_name = models.CharField(max_length=160)
    passenger_email = models.EmailField()
    passenger_phone = models.CharField(max_length=20, blank=True)
    passenger_document = models.CharField(
        max_length=50, 
        blank=True,
        help_text="Número de pasaporte o documento de identidad"
    )
    
    # Totales
    subtotal = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    tax = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    service_fee = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    total = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        indexes = [
            models.Index(fields=['booking_number']),
            models.Index(fields=['user', 'status']),
        ]
    
    def __str__(self):
        return f'Reserva #{self.booking_number or self.id} - {self.passenger_name}'
    
    @property
    def total_passengers(self):
        """Retorna el total de pasajeros en la reserva"""
        return self.passengers.count()


class BookingDetail(models.Model):
    """Modelo para representar los detalles de cada vuelo en una reserva"""
    booking = models.ForeignKey(
        Booking, 
        on_delete=models.CASCADE, 
        related_name='passengers'
    )
    flight = models.ForeignKey(
        'catalog.Flight',
        on_delete=models.PROTECT,
        related_name='bookings'
    )
    
    # Información del pasajero
    passenger_name = models.CharField(max_length=160)
    passenger_document = models.CharField(max_length=50)
    passenger_age = models.PositiveIntegerField(
        null=True, 
        blank=True,
        help_text="Edad del pasajero"
    )
    
    PASSENGER_TYPE_CHOICES = [
        ('ADULT', 'Adulto'),
        ('CHILD', 'Niño'),
        ('INFANT', 'Infante'),
    ]
    passenger_type = models.CharField(
        max_length=10,
        choices=PASSENGER_TYPE_CHOICES,
        default='ADULT'
    )
    
    # Información del asiento
    seat_number = models.CharField(
        max_length=10, 
        blank=True,
        help_text="Número de asiento (ej: 12A, 23F)"
    )
    
    # Equipaje
    checked_bags = models.PositiveIntegerField(
        default=0,
        help_text="Número de maletas documentadas"
    )
    carry_on_bags = models.PositiveIntegerField(
        default=1,
        help_text="Número de maletas de mano"
    )
    
    # Precios
    base_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    baggage_fee = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    total_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Detalle de Reserva"
        verbose_name_plural = "Detalles de Reserva"
        unique_together = ['flight', 'seat_number']
        indexes = [
            models.Index(fields=['booking', 'flight']),
        ]
    
    def __str__(self):
        return f'{self.passenger_name} - {self.flight}'
    
    def save(self, *args, **kwargs):
        """Calcula el precio total antes de guardar"""
        self.total_price = self.base_price + self.baggage_fee
        super().save(*args, **kwargs)
