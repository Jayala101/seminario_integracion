from django.db import models
from django.core.validators import MinValueValidator
from airlines.models import Airline


class Aircraft(models.Model):
    STATUS_CHOICES = [
        ('OPERATIONAL', 'Operacional'),
        ('MAINTENANCE', 'En Mantenimiento'),
        ('OUT_OF_SERVICE', 'Fuera de Servicio'),
        ('RETIRED', 'Retirada'),
    ]
    
    registration = models.CharField(max_length=20, unique=True, help_text="Matrícula")
    airline = models.ForeignKey(
        Airline,
        on_delete=models.PROTECT,
        related_name='aircrafts'
    )
    
    manufacturer = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year_manufactured = models.IntegerField(
        validators=[MinValueValidator(1900)]
    )
    
    total_seats = models.IntegerField(
        validators=[MinValueValidator(1)]
    )
    first_class_seats = models.IntegerField(default=0)
    business_class_seats = models.IntegerField(default=0)
    economy_class_seats = models.IntegerField(default=0)
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='OPERATIONAL'
    )
    flight_hours = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )
    total_flights = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )
    
    last_maintenance = models.DateField(null=True, blank=True)
    next_maintenance = models.DateField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['airline', 'registration']
        verbose_name = 'Aeronave'
        verbose_name_plural = 'Aeronaves'
        indexes = [
            models.Index(fields=['registration']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.registration} - {self.manufacturer} {self.model}"


class MaintenanceRecord(models.Model):
    MAINTENANCE_TYPE_CHOICES = [
        ('ROUTINE', 'Rutinario'),
        ('PREVENTIVE', 'Preventivo'),
        ('CORRECTIVE', 'Correctivo'),
        ('INSPECTION', 'Inspección'),
        ('REPAIR', 'Reparación'),
        ('OVERHAUL', 'Revisión General'),
    ]
    
    PRIORITY_CHOICES = [
        ('LOW', 'Baja'),
        ('MEDIUM', 'Media'),
        ('HIGH', 'Alta'),
        ('CRITICAL', 'Crítica'),
    ]
    
    STATUS_CHOICES = [
        ('SCHEDULED', 'Programado'),
        ('IN_PROGRESS', 'En Progreso'),
        ('COMPLETED', 'Completado'),
        ('CANCELLED', 'Cancelado'),
    ]
    
    aircraft = models.ForeignKey(
        Aircraft,
        on_delete=models.CASCADE,
        related_name='maintenance_records'
    )
    
    maintenance_type = models.CharField(
        max_length=20,
        choices=MAINTENANCE_TYPE_CHOICES
    )
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='MEDIUM'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='SCHEDULED'
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    findings = models.TextField(blank=True, help_text="Hallazgos durante el mantenimiento")
    actions_taken = models.TextField(blank=True, help_text="Acciones realizadas")
    
    technician = models.CharField(max_length=100)
    supervisor = models.CharField(max_length=100, blank=True)
    
    scheduled_date = models.DateField()
    start_date = models.DateField(null=True, blank=True)
    completion_date = models.DateField(null=True, blank=True)
    
    estimated_hours = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    actual_hours = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )
    
    parts_used = models.TextField(blank=True, help_text="Partes y materiales utilizados")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-scheduled_date']
        verbose_name = 'Registro de Mantenimiento'
        verbose_name_plural = 'Registros de Mantenimiento'
        indexes = [
            models.Index(fields=['aircraft', 'status']),
            models.Index(fields=['-scheduled_date']),
        ]
    
    def __str__(self):
        return f"{self.aircraft.registration} - {self.title} ({self.scheduled_date})"
