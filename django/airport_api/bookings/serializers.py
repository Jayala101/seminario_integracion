from rest_framework import serializers
from .models import Booking
from flights.serializers import FlightSerializer
from passengers.serializers import PassengerSerializer
from django.utils import timezone


class BookingSerializer(serializers.ModelSerializer):
    passenger_name = serializers.CharField(source='passenger.full_name', read_only=True)
    flight_number = serializers.CharField(source='flight.flight_number', read_only=True)
    flight_details = FlightSerializer(source='flight', read_only=True)
    passenger_details = PassengerSerializer(source='passenger', read_only=True)
    is_active = serializers.ReadOnlyField()
    
    class Meta:
        model = Booking
        fields = [
            'id', 'booking_code', 'passenger', 'passenger_name', 'passenger_details',
            'flight', 'flight_number', 'flight_details', 'booking_date',
            'travel_class', 'seat_number', 'checked_baggage', 'carry_on_baggage',
            'status', 'payment_method', 'amount_paid', 'special_requests',
            'meal_preference', 'is_active', 'created_at', 'updated_at', 'cancelled_at'
        ]
        read_only_fields = ['booking_code', 'booking_date', 'created_at', 'updated_at', 'cancelled_at']
    
    def validate(self, data):
        flight = data.get('flight')
        passenger = data.get('passenger')
        status = data.get('status', 'PENDING')
        
        if flight and flight.available_seats <= 0 and status in ['PENDING', 'CONFIRMED', 'PAID']:
            raise serializers.ValidationError({
                'flight': 'No hay asientos disponibles en este vuelo'
            })
        
        if flight and passenger:
            existing = Booking.objects.filter(
                flight=flight,
                passenger=passenger,
                status__in=['PENDING', 'CONFIRMED', 'PAID']
            )
            if self.instance:
                existing = existing.exclude(pk=self.instance.pk)
            
            if existing.exists():
                raise serializers.ValidationError({
                    'passenger': 'El pasajero ya tiene una reserva en este vuelo'
                })
        
        if flight and flight.departure_time < timezone.now():
            raise serializers.ValidationError({
                'flight': 'No se puede reservar un vuelo que ya partió'
            })
        
        return data
    
    def validate_amount_paid(self, value):
        if value < 0:
            raise serializers.ValidationError("El monto no puede ser negativo")
        return value


class BookingCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Booking
        fields = [
            'passenger', 'flight', 'travel_class', 'seat_number',
            'checked_baggage', 'carry_on_baggage', 'special_requests',
            'meal_preference'
        ]
