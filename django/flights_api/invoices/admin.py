from django.contrib import admin
from .models import Booking, BookingDetail


class BookingDetailInline(admin.TabularInline):
    model = BookingDetail
    extra = 1
    fields = [
        'flight', 'passenger_name', 'passenger_document', 'passenger_type',
        'seat_number', 'checked_bags', 'base_price', 'baggage_fee', 'total_price'
    ]
    readonly_fields = ['total_price']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = [
        'booking_number', 'passenger_name', 'user', 'status',
        'total', 'created_at', 'confirmed_at'
    ]
    list_filter = ['status', 'created_at', 'confirmed_at']
    search_fields = ['booking_number', 'passenger_name', 'passenger_email', 'user__username']
    readonly_fields = ['booking_number', 'subtotal', 'tax', 'service_fee', 'total', 'confirmed_at']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    inlines = [BookingDetailInline]
    
    fieldsets = (
        ('Información de la Reserva', {
            'fields': ('booking_number', 'user', 'status')
        }),
        ('Información del Pasajero Principal', {
            'fields': ('passenger_name', 'passenger_email', 'passenger_phone', 'passenger_document')
        }),
        ('Totales', {
            'fields': ('subtotal', 'tax', 'service_fee', 'total')
        }),
        ('Fechas', {
            'fields': ('created_at', 'confirmed_at')
        }),
    )


@admin.register(BookingDetail)
class BookingDetailAdmin(admin.ModelAdmin):
    list_display = [
        'booking', 'passenger_name', 'flight', 'seat_number',
        'passenger_type', 'total_price', 'created_at'
    ]
    list_filter = ['passenger_type', 'created_at']
    search_fields = ['passenger_name', 'passenger_document', 'booking__booking_number']
    raw_id_fields = ['booking', 'flight']
    readonly_fields = ['total_price']
