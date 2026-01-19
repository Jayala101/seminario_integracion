from rest_framework import serializers
from .models import Aircraft, MaintenanceRecord
from airlines.serializers import AirlineSerializer


class AircraftSerializer(serializers.ModelSerializer):
    airline_name = serializers.CharField(source='airline.name', read_only=True)
    airline_details = AirlineSerializer(source='airline', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    maintenance_count = serializers.SerializerMethodField()
    pending_maintenance = serializers.SerializerMethodField()
    
    class Meta:
        model = Aircraft
        fields = [
            'id', 'registration', 'airline', 'airline_name', 'airline_details',
            'manufacturer', 'model', 'year_manufactured', 'total_seats',
            'first_class_seats', 'business_class_seats', 'economy_class_seats',
            'status', 'status_display', 'flight_hours', 'total_flights',
            'last_maintenance', 'next_maintenance', 'maintenance_count',
            'pending_maintenance', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_maintenance_count(self, obj):
        return obj.maintenance_records.count()
    
    def get_pending_maintenance(self, obj):
        return obj.maintenance_records.filter(
            status__in=['SCHEDULED', 'IN_PROGRESS']
        ).count()
    
    def validate(self, data):
        total = data.get('total_seats', 0)
        first = data.get('first_class_seats', 0)
        business = data.get('business_class_seats', 0)
        economy = data.get('economy_class_seats', 0)
        
        if total and (first + business + economy) != total:
            raise serializers.ValidationError(
                'La suma de asientos por clase debe ser igual al total de asientos'
            )
        
        return data


class MaintenanceRecordSerializer(serializers.ModelSerializer):
    aircraft_registration = serializers.CharField(source='aircraft.registration', read_only=True)
    maintenance_type_display = serializers.CharField(source='get_maintenance_type_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    aircraft_details = AircraftSerializer(source='aircraft', read_only=True)
    duration_days = serializers.SerializerMethodField()
    
    class Meta:
        model = MaintenanceRecord
        fields = [
            'id', 'aircraft', 'aircraft_registration', 'aircraft_details',
            'maintenance_type', 'maintenance_type_display', 'priority',
            'priority_display', 'status', 'status_display', 'title',
            'description', 'findings', 'actions_taken', 'technician',
            'supervisor', 'scheduled_date', 'start_date', 'completion_date',
            'duration_days', 'estimated_hours', 'actual_hours', 'cost',
            'parts_used', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_duration_days(self, obj):
        if obj.start_date and obj.completion_date:
            return (obj.completion_date - obj.start_date).days
        return None
    
    def validate(self, data):
        start = data.get('start_date')
        completion = data.get('completion_date')
        scheduled = data.get('scheduled_date')
        
        if start and completion and start > completion:
            raise serializers.ValidationError({
                'completion_date': 'La fecha de finalización debe ser posterior a la de inicio'
            })
        
        if start and scheduled and start < scheduled:
            raise serializers.ValidationError({
                'start_date': 'La fecha de inicio no puede ser anterior a la programada'
            })
        
        return data
