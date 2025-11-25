from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """Perfil extendido para usuarios/pasajeros"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Información personal
    phone = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    
    # Documento de identidad
    document_type = models.CharField(
        max_length=20,
        choices=[
            ('PASSPORT', 'Pasaporte'),
            ('ID_CARD', 'Cédula/DNI'),
            ('DRIVER_LICENSE', 'Licencia de Conducir'),
        ],
        default='PASSPORT'
    )
    document_number = models.CharField(max_length=50, blank=True)
    document_expiry = models.DateField(null=True, blank=True)
    
    # Dirección
    address = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    
    # Preferencias de viaje
    frequent_flyer_number = models.CharField(max_length=50, blank=True)
    preferred_seat = models.CharField(
        max_length=20,
        choices=[
            ('WINDOW', 'Ventana'),
            ('AISLE', 'Pasillo'),
            ('MIDDLE', 'Medio'),
        ],
        blank=True
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuario"
    
    def __str__(self):
        return f"Perfil de {self.user.username}"
