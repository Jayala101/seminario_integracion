from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Airport(models.Model):
    code = models.CharField(
        max_length=3,
        unique=True,
        help_text="Código IATA (ej: MEX, JFK, LAX)"
    )
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
        null=True,
        blank=True
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
        null=True,
        blank=True
    )
    elevation = models.IntegerField(
        null=True,
        blank=True,
        help_text="Elevación en metros"
    )
    
    timezone = models.CharField(max_length=50, blank=True)
    terminals = models.PositiveIntegerField(default=1)
    runways = models.PositiveIntegerField(default=1)
    annual_passengers = models.PositiveIntegerField(
        default=0,
        help_text="Pasajeros anuales (aprox.)"
    )
    
    is_international = models.BooleanField(default=True)
    is_cargo = models.BooleanField(default=False, help_text="Acepta carga")
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Aeropuerto'
        verbose_name_plural = 'Aeropuertos'
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['city', 'country']),
        ]
    
    def __str__(self):
        return f"{self.code} - {self.name} ({self.city})"
