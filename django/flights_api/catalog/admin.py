from django.contrib import admin
from .models import Airline, Flight


@admin.register(Airline)
class AirlineAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'country', 'is_active', 'created_at']
    list_filter = ['is_active', 'country']
    search_fields = ['name', 'code', 'country']
    ordering = ['name']


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = [
        'flight_number', 'airline', 'origin_airport', 'destination_airport',
        'departure_time', 'status', 'available_seats', 'is_active'
    ]
    list_filter = ['status', 'flight_class', 'is_active', 'airline']
    search_fields = ['flight_number', 'airline__name', 'airline__code']
    date_hierarchy = 'departure_time'
    ordering = ['-departure_time']
    raw_id_fields = ['airline', 'origin_airport', 'destination_airport']
