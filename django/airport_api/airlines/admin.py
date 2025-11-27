from django.contrib import admin
from .models import Airline


@admin.register(Airline)
class AirlineAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'country', 'fleet_size', 'is_active', 'created_at']
    list_filter = ['is_active', 'country', 'founded_year']
    search_fields = ['name', 'code', 'country']
    ordering = ['name']
    list_per_page = 25
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('code', 'name', 'country', 'founded_year')
        }),
        ('Detalles Operativos', {
            'fields': ('fleet_size', 'headquarters', 'website', 'logo')
        }),
        ('Estado', {
            'fields': ('is_active',)
        }),
    )
