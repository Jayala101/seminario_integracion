from django.contrib import admin
from .models import Airport


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = [
        'code', 'name', 'city', 'country', 
        'is_international', 'is_active', 'created_at'
    ]
    list_filter = ['is_international', 'is_active', 'country']
    search_fields = ['name', 'code', 'city', 'country']
    ordering = ['name']
    fieldsets = (
        ('Información Básica', {
            'fields': ('code', 'name', 'city', 'country', 'timezone')
        }),
        ('Ubicación Geográfica', {
            'fields': ('latitude', 'longitude', 'elevation')
        }),
        ('Información Adicional', {
            'fields': ('website', 'is_international', 'is_active')
        }),
    )
