from django.contrib import admin
from .models import Passenger


@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = [
        'full_name', 'document_number', 'email', 'nationality',
        'is_active', 'created_at'
    ]
    list_filter = ['is_active', 'document_type', 'nationality', 'gender']
    search_fields = ['first_name', 'last_name', 'document_number', 'email']
    ordering = ['last_name', 'first_name']
    list_per_page = 25
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('first_name', 'last_name', 'date_of_birth', 'nationality', 'gender')
        }),
        ('Documento de Identidad', {
            'fields': ('document_type', 'document_number', 'document_expiry')
        }),
        ('Contacto', {
            'fields': ('email', 'phone')
        }),
        ('Dirección', {
            'fields': ('address', 'city', 'country', 'postal_code')
        }),
        ('Preferencias', {
            'fields': ('frequent_flyer_number', 'special_needs')
        }),
        ('Sistema', {
            'fields': ('user', 'is_active')
        }),
    )
