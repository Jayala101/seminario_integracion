from django.contrib import admin
from .models import CrewMember, FlightCrewAssignment


@admin.register(CrewMember)
class CrewMemberAdmin(admin.ModelAdmin):
    list_display = [
        'employee_id', 'full_name', 'role', 'status',
        'is_available', 'flight_hours', 'license_expiry'
    ]
    list_filter = ['role', 'status', 'is_available', 'nationality']
    search_fields = ['employee_id', 'first_name', 'last_name', 'email']
    ordering = ['last_name', 'first_name']
    list_per_page = 25
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('employee_id', 'first_name', 'last_name', 'date_of_birth', 'nationality')
        }),
        ('Información Profesional', {
            'fields': ('role', 'license_number', 'license_expiry', 'hire_date',
                      'years_of_experience', 'flight_hours')
        }),
        ('Contacto', {
            'fields': ('email', 'phone', 'emergency_contact', 'emergency_phone')
        }),
        ('Certificaciones', {
            'fields': ('certifications', 'languages')
        }),
        ('Estado', {
            'fields': ('status', 'is_available')
        }),
    )


@admin.register(FlightCrewAssignment)
class FlightCrewAssignmentAdmin(admin.ModelAdmin):
    list_display = ['flight', 'crew_member', 'assigned_at']
    list_filter = ['crew_member__role', 'assigned_at']
    search_fields = ['flight__flight_number', 'crew_member__first_name', 'crew_member__last_name']
    ordering = ['-assigned_at']
    list_per_page = 25
    
    fieldsets = (
        ('Asignación', {
            'fields': ('flight', 'crew_member', 'notes')
        }),
        ('Información', {
            'fields': ('assigned_at',),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['assigned_at']
