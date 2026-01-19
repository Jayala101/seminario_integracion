from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """Modelo de perfil de usuario con roles"""
    ROLE_CHOICES = [
        ('ADMIN', 'Administrador'),
        ('STAFF', 'Personal'),
        ('CUSTOMER', 'Cliente'),
    ]
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='CUSTOMER'
    )
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Perfil de Usuario'
        verbose_name_plural = 'Perfiles de Usuario'
    
    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"
    
    @property
    def is_admin(self):
        return self.role == 'ADMIN' or self.user.is_superuser
    
    @property
    def is_staff_member(self):
        return self.role in ['ADMIN', 'STAFF'] or self.user.is_staff


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Crea automáticamente un perfil cuando se crea un usuario"""
    if created:
        # Si es superusuario, crear perfil de admin
        role = 'ADMIN' if instance.is_superuser else 'CUSTOMER'
        UserProfile.objects.create(user=instance, role=role)
        
        # Crear automáticamente un pasajero para el usuario si no existe
        if not hasattr(instance, 'passenger_profile'):
            Passenger.objects.create(
                user=instance,
                first_name=instance.first_name or instance.username,
                last_name=instance.last_name or '',
                date_of_birth='2000-01-01',  # Fecha por defecto, se puede actualizar después
                nationality='México',
                document_type='ID_CARD',
                document_number=f'USR{instance.id:08d}',
                email=instance.email or f'{instance.username}@example.com',
                phone='+5200000000000',
            )


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Guarda el perfil cuando se guarda el usuario"""
    if hasattr(instance, 'profile'):
        instance.profile.save()


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
