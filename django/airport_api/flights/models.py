from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class Flight(models.Model):
    STATUS_CHOICES = [
        ('SCHEDULED', 'Programado'),
        ('BOARDING', 'Abordando'),
        ('DEPARTED', 'Despegado'),
        ('IN_FLIGHT', 'En Vuelo'),
        ('LANDED', 'Aterrizado'),
        ('ARRIVED', 'Arribado'),
        ('CANCELLED', 'Cancelado'),
        ('DELAYED', 'Retrasado'),
    ]
    
    CLASS_CHOICES = [
        ('ECONOMY', 'Económica'),
        ('PREMIUM_ECONOMY', 'Premium Económica'),
        ('BUSINESS', 'Ejecutiva'),
        ('FIRST', 'Primera Clase'),
    ]
    
    airline = models.ForeignKey(
        'airlines.Airline',
        on_delete=models.PROTECT,
        related_name='flights'
    )
    origin_airport = models.ForeignKey(
        'airports.Airport',
        on_delete=models.PROTECT,
        related_name='departures'
    )
    destination_airport = models.ForeignKey(
        'airports.Airport',
        on_delete=models.PROTECT,
        related_name='arrivals'
    )
    
    flight_number = models.CharField(max_length=10)
    aircraft_type = models.CharField(max_length=50, help_text="Tipo de aeronave")
    
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    
    total_seats = models.PositiveIntegerField(default=180)
    available_seats = models.PositiveIntegerField(default=180)
    base_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    
    flight_class = models.CharField(max_length=20, choices=CLASS_CHOICES, default='ECONOMY')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SCHEDULED')
    gate = models.CharField(max_length=10, blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-departure_time']
        verbose_name = 'Vuelo'
        verbose_name_plural = 'Vuelos'
        unique_together = ['airline', 'flight_number', 'departure_time']
        indexes = [
            models.Index(fields=['flight_number', 'departure_time']),
            models.Index(fields=['origin_airport', 'destination_airport']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.airline.code}{self.flight_number} - {self.origin_airport.code} → {self.destination_airport.code}"
    
    @property
    def duration(self):
        return self.arrival_time - self.departure_time
    
    @property
    def occupancy_rate(self):
        if self.total_seats == 0:
            return 0
        occupied = self.total_seats - self.available_seats
        return (occupied / self.total_seats) * 100
