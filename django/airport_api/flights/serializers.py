from rest_framework import serializers
from .models import Flight
from airlines.serializers import AirlineSerializer
from airports.serializers import AirportSerializer


class FlightSerializer(serializers.ModelSerializer):
    airline_details = AirlineSerializer(source='airline', read_only=True)
    origin_details = AirportSerializer(source='origin_airport', read_only=True)
    destination_details = AirportSerializer(source='destination_airport', read_only=True)
    duration = serializers.ReadOnlyField()
    occupancy_rate = serializers.ReadOnlyField()
    
    class Meta:
        model = Flight
        fields = [
            'id', 'airline', 'airline_details', 'flight_number',
            'origin_airport', 'origin_details',
            'destination_airport', 'destination_details',
            'departure_time', 'arrival_time', 'duration',
            'aircraft_type', 'total_seats', 'available_seats',
            'base_price', 'flight_class', 'status', 'gate',
            'occupancy_rate', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def validate(self, data):
        if data.get('departure_time') and data.get('arrival_time'):
            if data['arrival_time'] <= data['departure_time']:
                raise serializers.ValidationError(
                    "La hora de llegada debe ser posterior a la de salida"
                )
        
        if data.get('origin_airport') == data.get('destination_airport'):
            raise serializers.ValidationError(
                "El aeropuerto de origen y destino no pueden ser el mismo"
            )
        
        if data.get('available_seats', 0) > data.get('total_seats', 0):
            raise serializers.ValidationError(
                "Los asientos disponibles no pueden exceder el total"
            )
        
        return data
