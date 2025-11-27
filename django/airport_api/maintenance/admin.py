from django.contrib import admin
from .models import Aircraft, MaintenanceRecord


@admin.register(Aircraft)
class AircraftAdmin(admin.ModelAdmin):
    list_display = [
        'registration', 'airline', 'manufacturer', 'model',
        'status', 'flight_hours', 'next_maintenance'
    ]
    list_filter = ['status', 'manufacturer', 'airline']
    search_fields = ['registration', 'manufacturer', 'model']
    ordering = ['airline', 'registration']
    list_per_page = 25
    
    fieldsets = (
        ('Identificación', {
            'fields': ('registration', 'airline')
        }),
        ('Especificaciones', {
            'fields': ('manufacturer', 'model', 'year_manufactured')
        }),
        ('Capacidad', {
            'fields': ('total_seats', 'first_class_seats', 'business_class_seats', 'economy_class_seats')
        }),
        ('Operación', {
            'fields': ('status', 'flight_hours', 'total_flights')
        }),
        ('Mantenimiento', {
            'fields': ('last_maintenance', 'next_maintenance')
        }),
    )


@admin.register(MaintenanceRecord)
class MaintenanceRecordAdmin(admin.ModelAdmin):
    list_display = [
        'aircraft', 'title', 'maintenance_type', 'priority',
        'status', 'scheduled_date', 'technician'
    ]
    list_filter = ['status', 'maintenance_type', 'priority', 'scheduled_date']
    search_fields = ['title', 'description', 'technician', 'aircraft__registration']
    ordering = ['-scheduled_date']
    list_per_page = 25
    
    fieldsets = (
        ('Aeronave', {
            'fields': ('aircraft',)
        }),
        ('Detalles', {
            'fields': ('maintenance_type', 'priority', 'status', 'title', 'description')
        }),
        ('Personal', {
            'fields': ('technician', 'supervisor')
        }),
        ('Fechas', {
            'fields': ('scheduled_date', 'start_date', 'completion_date')
        }),
        ('Recursos', {
            'fields': ('estimated_hours', 'actual_hours', 'cost', 'parts_used')
        }),
        ('Resultados', {
            'fields': ('findings', 'actions_taken'),
            'classes': ('collapse',)
        }),
    )
