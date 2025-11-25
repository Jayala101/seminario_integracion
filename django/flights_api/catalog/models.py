from django.db import models


class Airline(models.Model):
    """Modelo para representar aerolíneas"""
    code = models.CharField(
        max_length=10, 
        unique=True, 
        help_text="Código IATA de la aerolínea (ej: AA, UA, DL, AM)"
    )
    name = models.CharField(max_length=120, unique=True)
    country = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    logo_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "Aerolínea"
        verbose_name_plural = "Aerolíneas"

    def __str__(self):
        return f"{self.code} - {self.name}"


class Flight(models.Model):
    """Modelo para representar vuelos"""
    CLASS_CHOICES = [
        ('ECONOMY', 'Económica'),
        ('PREMIUM_ECONOMY', 'Económica Premium'),
        ('BUSINESS', 'Ejecutiva'),
        ('FIRST', 'Primera Clase'),
    ]
    
    STATUS_CHOICES = [
        ('SCHEDULED', 'Programado'),
        ('BOARDING', 'Abordando'),
        ('DEPARTED', 'Despegado'),
        ('IN_FLIGHT', 'En Vuelo'),
        ('ARRIVED', 'Arribado'),
        ('CANCELLED', 'Cancelado'),
        ('DELAYED', 'Retrasado'),
    ]
    
    airline = models.ForeignKey(
        Airline, 
        on_delete=models.CASCADE, 
        related_name="flights"
    )
    flight_number = models.CharField(
        max_length=20, 
        help_text="Número de vuelo (ej: AA100, AM456)"
    )
    origin_airport = models.ForeignKey(
        'warehouses.Airport', 
        on_delete=models.PROTECT, 
        related_name="departures"
    )
    destination_airport = models.ForeignKey(
        'warehouses.Airport', 
        on_delete=models.PROTECT, 
        related_name="arrivals"
    )
    
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    
    base_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        help_text="Precio base del vuelo en USD"
    )
    available_seats = models.PositiveIntegerField(default=0)
    total_seats = models.PositiveIntegerField(default=180)
    
    flight_class = models.CharField(
        max_length=20, 
        choices=CLASS_CHOICES, 
        default='ECONOMY'
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='SCHEDULED'
    )
    
    aircraft_type = models.CharField(max_length=50, blank=True, help_text="Tipo de aeronave (ej: Boeing 737, Airbus A320)")
    gate = models.CharField(max_length=10, blank=True, help_text="Puerta de embarque")
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-departure_time",)
        verbose_name = "Vuelo"
        verbose_name_plural = "Vuelos"
        indexes = [
            models.Index(fields=['flight_number', 'departure_time']),
            models.Index(fields=['origin_airport', 'destination_airport']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.airline.code}{self.flight_number} - {self.origin_airport.code} → {self.destination_airport.code}"
    
    @property
    def duration(self):
        """Calcula la duración del vuelo"""
        return self.arrival_time - self.departure_time
    
    @property
    def is_full(self):
        """Verifica si el vuelo está lleno"""
        return self.available_seats == 0
    
    @property
    def occupancy_percentage(self):
        """Calcula el porcentaje de ocupación"""
        if self.total_seats == 0:
            return 0
        occupied = self.total_seats - self.available_seats
        return (occupied / self.total_seats) * 100
