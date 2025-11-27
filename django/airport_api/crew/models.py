from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from flights.models import Flight


class CrewMember(models.Model):
    ROLE_CHOICES = [
        ('CAPTAIN', 'Capitán'),
        ('FIRST_OFFICER', 'Primer Oficial'),
        ('FLIGHT_ENGINEER', 'Ingeniero de Vuelo'),
        ('FLIGHT_ATTENDANT', 'Asistente de Vuelo'),
        ('PURSER', 'Jefe de Cabina'),
    ]
    
    STATUS_CHOICES = [
        ('ACTIVE', 'Activo'),
        ('ON_LEAVE', 'De Licencia'),
        ('SUSPENDED', 'Suspendido'),
        ('RETIRED', 'Retirado'),
    ]
    
    employee_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    nationality = models.CharField(max_length=100)
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    license_number = models.CharField(max_length=50, unique=True)
    license_expiry = models.DateField()
    
    hire_date = models.DateField()
    years_of_experience = models.IntegerField(
        validators=[MinValueValidator(0)]
    )
    flight_hours = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )
    
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    emergency_contact = models.CharField(max_length=100)
    emergency_phone = models.CharField(max_length=20)
    
    certifications = models.TextField(blank=True, help_text="Certificaciones adicionales")
    languages = models.CharField(max_length=200, help_text="Idiomas (separados por coma)")
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='ACTIVE'
    )
    is_available = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'Miembro de Tripulación'
        verbose_name_plural = 'Miembros de Tripulación'
        indexes = [
            models.Index(fields=['employee_id']),
            models.Index(fields=['role']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.get_role_display()} {self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def total_assignments(self):
        return self.flight_assignments.count()


class FlightCrewAssignment(models.Model):
    flight = models.ForeignKey(
        Flight,
        on_delete=models.CASCADE,
        related_name='crew_assignments'
    )
    crew_member = models.ForeignKey(
        CrewMember,
        on_delete=models.PROTECT,
        related_name='flight_assignments'
    )
    
    assigned_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['flight__departure_time', 'crew_member__role']
        verbose_name = 'Asignación de Tripulación'
        verbose_name_plural = 'Asignaciones de Tripulación'
        unique_together = ['flight', 'crew_member']
        indexes = [
            models.Index(fields=['flight', 'crew_member']),
        ]
    
    def __str__(self):
        return f"{self.crew_member.full_name} - {self.flight.flight_number}"
