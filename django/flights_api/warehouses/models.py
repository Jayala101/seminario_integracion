from django.db import models


class Airport(models.Model):
    """Modelo para representar aeropuertos"""
    code = models.CharField(
        max_length=10, 
        unique=True, 
        help_text="Código IATA del aeropuerto (ej: JFK, LAX, MEX, CDG)"
    )
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    timezone = models.CharField(
        max_length=50, 
        blank=True,
        help_text="Zona horaria del aeropuerto (ej: America/New_York)"
    )
    
    # Coordenadas geográficas
    latitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True
    )
    longitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True
    )
    
    # Información adicional
    elevation = models.IntegerField(
        null=True, 
        blank=True,
        help_text="Elevación en metros sobre el nivel del mar"
    )
    website = models.URLField(blank=True)
    
    # Estado del aeropuerto
    is_international = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = "Aeropuerto"
        verbose_name_plural = "Aeropuertos"
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['city', 'country']),
        ]
    
    def __str__(self):
        return f"{self.code} - {self.name} ({self.city})"
    
    @property
    def full_location(self):
        """Retorna la ubicación completa del aeropuerto"""
        return f"{self.city}, {self.country}"
