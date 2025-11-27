from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Passenger(models.Model):
    DOCUMENT_TYPE_CHOICES = [
        ('PASSPORT', 'Pasaporte'),
        ('ID_CARD', 'Cédula/DNI'),
        ('DRIVER_LICENSE', 'Licencia de Conducir'),
    ]
    
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='passenger_profile'
    )
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    nationality = models.CharField(max_length=100)
    gender = models.CharField(
        max_length=10,
        choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')],
        blank=True
    )
    
    document_type = models.CharField(
        max_length=20,
        choices=DOCUMENT_TYPE_CHOICES,
        default='PASSPORT'
    )
    document_number = models.CharField(
        max_length=50,
        unique=True,
        validators=[RegexValidator(r'^[A-Z0-9]+$', 'Solo letras mayúsculas y números')]
    )
    document_expiry = models.DateField(null=True, blank=True)
    
    email = models.EmailField()
    phone = models.CharField(
        max_length=20,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', 'Número de teléfono inválido')]
    )
    
    address = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    
    frequent_flyer_number = models.CharField(max_length=50, blank=True)
    special_needs = models.TextField(blank=True, help_text="Necesidades especiales")
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'Pasajero'
        verbose_name_plural = 'Pasajeros'
        indexes = [
            models.Index(fields=['document_number']),
            models.Index(fields=['email']),
        ]
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.document_number})"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
