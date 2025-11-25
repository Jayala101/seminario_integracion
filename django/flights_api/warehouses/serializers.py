from rest_framework import serializers
from .models import Airport


class AirportSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Airport"""
    full_location = serializers.ReadOnlyField()
    departures_count = serializers.SerializerMethodField()
    arrivals_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Airport
        fields = [
            'id', 'code', 'name', 'city', 'country', 'timezone',
            'latitude', 'longitude', 'elevation', 'website',
            'is_international', 'is_active', 'full_location',
            'departures_count', 'arrivals_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_departures_count(self, obj):
        """Cuenta de vuelos que salen de este aeropuerto"""
        return obj.departures.filter(is_active=True).count()
    
    def get_arrivals_count(self, obj):
        """Cuenta de vuelos que llegan a este aeropuerto"""
        return obj.arrivals.filter(is_active=True).count()


class AirportListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listado de aeropuertos"""
    full_location = serializers.ReadOnlyField()
    
    class Meta:
        model = Airport
        fields = [
            'id', 'code', 'name', 'city', 'country',
            'full_location', 'is_international', 'is_active'
        ]
