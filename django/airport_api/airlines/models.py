from django.db import models
from django.core.validators import RegexValidator


class Airline(models.Model):
    code = models.CharField(
        max_length=3,
        unique=True,
        validators=[RegexValidator(r'^[A-Z]{2,3}$', 'Código debe ser 2-3 letras mayúsculas')],
        help_text="Código IATA (ej: AM, AA, DL)"
    )
    name = models.CharField(max_length=150)
    country = models.CharField(max_length=100)
    founded_year = models.PositiveIntegerField(null=True, blank=True)
    fleet_size = models.PositiveIntegerField(default=0, help_text="Número de aeronaves")
    headquarters = models.CharField(max_length=200, blank=True)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='airlines/logos/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Aerolínea'
        verbose_name_plural = 'Aerolíneas'
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['country']),
        ]
    
    def __str__(self):
        return f"{self.code} - {self.name}"
