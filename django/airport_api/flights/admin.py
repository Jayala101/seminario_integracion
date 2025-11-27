from django.contrib import admin
from .models import Flight


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = [
        'flight_number', 'airline', 'origin_airport', 'destination_airport',
        'departure_time', 'status', 'available_seats', 'is_active'
    ]
    list_filter = ['status', 'flight_class', 'is_active', 'airline']
    search_fields = ['flight_number', 'airline__name', 'aircraft_type']
    date_hierarchy = 'departure_time'
    ordering = ['-departure_time']
    list_per_page = 25
    raw_id_fields = ['airline', 'origin_airport', 'destination_airport']
    
    fieldsets = (
        ('Información del Vuelo', {
            'fields': ('airline', 'flight_number', 'aircraft_type')
        }),
        ('Ruta', {
            'fields': ('origin_airport', 'destination_airport')
        }),
        ('Horarios', {
            'fields': ('departure_time', 'arrival_time')
        }),
        ('Capacidad y Precios', {
            'fields': ('total_seats', 'available_seats', 'base_price', 'flight_class')
        }),
        ('Estado', {
            'fields': ('status', 'gate', 'is_active')
        }),
    )
