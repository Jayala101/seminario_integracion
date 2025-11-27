from rest_framework import serializers
from .models import Airline


class AirlineSerializer(serializers.ModelSerializer):
    flights_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Airline
        fields = [
            'id', 'code', 'name', 'country', 'founded_year', 'fleet_size',
            'headquarters', 'website', 'logo', 'is_active', 'flights_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_flights_count(self, obj):
        return obj.flights.filter(is_active=True).count()
    
    def validate_code(self, value):
        if not value.isupper():
            raise serializers.ValidationError("El código debe estar en mayúsculas")
        return value
    
    def validate_founded_year(self, value):
        if value and (value < 1900 or value > 2025):
            raise serializers.ValidationError("Año de fundación inválido")
        return value
