from rest_framework import serializers
from .models import Airline, Flight


class AirlineSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Airline"""
    flights_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Airline
        fields = [
            'id', 'code', 'name', 'country', 'website', 
            'logo_url', 'is_active', 'flights_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_flights_count(self, obj):
        return obj.flights.filter(is_active=True).count()


class FlightListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listado de vuelos"""
    airline_name = serializers.CharField(source='airline.name', read_only=True)
    airline_code = serializers.CharField(source='airline.code', read_only=True)
    origin_code = serializers.CharField(source='origin_airport.code', read_only=True)
    origin_city = serializers.CharField(source='origin_airport.city', read_only=True)
    destination_code = serializers.CharField(source='destination_airport.code', read_only=True)
    destination_city = serializers.CharField(source='destination_airport.city', read_only=True)
    duration = serializers.ReadOnlyField()
    is_full = serializers.ReadOnlyField()
    occupancy_percentage = serializers.ReadOnlyField()
    
    class Meta:
        model = Flight
        fields = [
            'id', 'flight_number', 'airline', 'airline_name', 'airline_code',
            'origin_airport', 'origin_code', 'origin_city',
            'destination_airport', 'destination_code', 'destination_city',
            'departure_time', 'arrival_time', 'duration',
            'base_price', 'available_seats', 'total_seats',
            'flight_class', 'status', 'is_full', 'occupancy_percentage'
        ]


class FlightDetailSerializer(serializers.ModelSerializer):
    """Serializer detallado para vuelos individuales"""
    airline = AirlineSerializer(read_only=True)
    airline_id = serializers.PrimaryKeyRelatedField(
        queryset=Airline.objects.all(),
        source='airline',
        write_only=True
    )
    origin_airport_details = serializers.SerializerMethodField()
    destination_airport_details = serializers.SerializerMethodField()
    duration = serializers.ReadOnlyField()
    is_full = serializers.ReadOnlyField()
    occupancy_percentage = serializers.ReadOnlyField()
    
    class Meta:
        model = Flight
        fields = [
            'id', 'flight_number', 'airline', 'airline_id',
            'origin_airport', 'origin_airport_details',
            'destination_airport', 'destination_airport_details',
            'departure_time', 'arrival_time', 'duration',
            'base_price', 'available_seats', 'total_seats',
            'flight_class', 'status', 'aircraft_type', 'gate',
            'is_full', 'occupancy_percentage', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_origin_airport_details(self, obj):
        return {
            'id': obj.origin_airport.id,
            'code': obj.origin_airport.code,
            'name': obj.origin_airport.name,
            'city': obj.origin_airport.city,
            'country': obj.origin_airport.country
        }
    
    def get_destination_airport_details(self, obj):
        return {
            'id': obj.destination_airport.id,
            'code': obj.destination_airport.code,
            'name': obj.destination_airport.name,
            'city': obj.destination_airport.city,
            'country': obj.destination_airport.country
        }
    
    def validate(self, data):
        """Validaciones personalizadas"""
        if data.get('departure_time') and data.get('arrival_time'):
            if data['arrival_time'] <= data['departure_time']:
                raise serializers.ValidationError(
                    "La hora de llegada debe ser posterior a la hora de salida"
                )
        
        if data.get('origin_airport') == data.get('destination_airport'):
            raise serializers.ValidationError(
                "El aeropuerto de origen y destino no pueden ser el mismo"
            )
        
        if data.get('available_seats', 0) > data.get('total_seats', 0):
            raise serializers.ValidationError(
                "Los asientos disponibles no pueden exceder el total de asientos"
            )
        
        return data
