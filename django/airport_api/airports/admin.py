from django.contrib import admin
from .models import Airport


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'city', 'country', 'terminals', 'is_international', 'is_active']
    list_filter = ['is_international', 'is_cargo', 'is_active', 'country']
    search_fields = ['name', 'code', 'city', 'country']
    ordering = ['name']
    list_per_page = 25
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('code', 'name', 'city', 'country')
        }),
        ('Ubicación Geográfica', {
            'fields': ('latitude', 'longitude', 'elevation', 'timezone')
        }),
        ('Información Operativa', {
            'fields': ('terminals', 'runways', 'annual_passengers')
        }),
        ('Clasificación', {
            'fields': ('is_international', 'is_cargo', 'is_active')
        }),
    )
