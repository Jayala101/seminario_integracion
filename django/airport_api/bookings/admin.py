from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = [
        'booking_code', 'passenger', 'flight', 'travel_class',
        'status', 'amount_paid', 'booking_date'
    ]
    list_filter = ['status', 'travel_class', 'booking_date', 'payment_method']
    search_fields = ['booking_code', 'passenger__first_name', 'passenger__last_name']
    ordering = ['-booking_date']
    list_per_page = 25
    readonly_fields = ['booking_code', 'booking_date', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Información General', {
            'fields': ('booking_code', 'passenger', 'flight', 'booking_date')
        }),
        ('Detalles del Viaje', {
            'fields': ('travel_class', 'seat_number', 'checked_baggage', 'carry_on_baggage')
        }),
        ('Pago', {
            'fields': ('status', 'payment_method', 'amount_paid')
        }),
        ('Preferencias', {
            'fields': ('special_requests', 'meal_preference')
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at', 'cancelled_at'),
            'classes': ('collapse',)
        }),
    )
