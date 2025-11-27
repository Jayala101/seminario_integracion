from rest_framework import serializers
from .models import CrewMember, FlightCrewAssignment
from django.utils import timezone


class CrewMemberSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    total_assignments = serializers.ReadOnlyField()
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = CrewMember
        fields = [
            'id', 'employee_id', 'first_name', 'last_name', 'full_name',
            'date_of_birth', 'nationality', 'role', 'role_display',
            'license_number', 'license_expiry', 'hire_date',
            'years_of_experience', 'flight_hours', 'email', 'phone',
            'emergency_contact', 'emergency_phone', 'certifications',
            'languages', 'status', 'status_display', 'is_available',
            'total_assignments', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def validate_license_expiry(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError("La licencia está vencida")
        return value
    
    def validate_email(self, value):
        if self.instance is None:
            if CrewMember.objects.filter(email=value).exists():
                raise serializers.ValidationError("Ya existe un miembro con este email")
        return value


class FlightCrewAssignmentSerializer(serializers.ModelSerializer):
    crew_member_name = serializers.CharField(source='crew_member.full_name', read_only=True)
    crew_member_role = serializers.CharField(source='crew_member.get_role_display', read_only=True)
    flight_number = serializers.CharField(source='flight.flight_number', read_only=True)
    crew_member_details = CrewMemberSerializer(source='crew_member', read_only=True)
    
    class Meta:
        model = FlightCrewAssignment
        fields = [
            'id', 'flight', 'flight_number', 'crew_member', 'crew_member_name',
            'crew_member_role', 'crew_member_details', 'assigned_at', 'notes'
        ]
        read_only_fields = ['assigned_at']
    
    def validate(self, data):
        crew_member = data.get('crew_member')
        flight = data.get('flight')
        
        if crew_member and crew_member.status != 'ACTIVE':
            raise serializers.ValidationError({
                'crew_member': 'El miembro de la tripulación no está activo'
            })
        
        if crew_member and not crew_member.is_available:
            raise serializers.ValidationError({
                'crew_member': 'El miembro de la tripulación no está disponible'
            })
        
        if crew_member and crew_member.license_expiry < timezone.now().date():
            raise serializers.ValidationError({
                'crew_member': 'La licencia del miembro ha expirado'
            })
        
        if flight and crew_member:
            existing = FlightCrewAssignment.objects.filter(
                flight=flight,
                crew_member=crew_member
            )
            if self.instance:
                existing = existing.exclude(pk=self.instance.pk)
            
            if existing.exists():
                raise serializers.ValidationError(
                    'Este miembro ya está asignado a este vuelo'
                )
        
        return data
