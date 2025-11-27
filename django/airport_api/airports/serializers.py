from rest_framework import serializers
from .models import Airport


class AirportSerializer(serializers.ModelSerializer):
    departures_count = serializers.SerializerMethodField()
    arrivals_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Airport
        fields = [
            'id', 'code', 'name', 'city', 'country',
            'latitude', 'longitude', 'elevation', 'timezone',
            'terminals', 'runways', 'annual_passengers',
            'is_international', 'is_cargo', 'is_active',
            'departures_count', 'arrivals_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_departures_count(self, obj):
        return obj.departures.filter(is_active=True).count()
    
    def get_arrivals_count(self, obj):
        return obj.arrivals.filter(is_active=True).count()
    
    def validate_code(self, value):
        if not value.isupper():
            raise serializers.ValidationError("El código debe estar en mayúsculas")
        if len(value) != 3:
            raise serializers.ValidationError("El código IATA debe tener 3 caracteres")
        return value
