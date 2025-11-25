from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Booking, BookingDetail
from catalog.serializers import FlightListSerializer


class BookingDetailSerializer(serializers.ModelSerializer):
    """Serializer para detalles de reserva"""
    flight_info = FlightListSerializer(source='flight', read_only=True)
    
    class Meta:
        model = BookingDetail
        fields = [
            'id', 'flight', 'flight_info',
            'passenger_name', 'passenger_document', 'passenger_age', 'passenger_type',
            'seat_number', 'checked_bags', 'carry_on_bags',
            'base_price', 'baggage_fee', 'total_price',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['total_price', 'created_at', 'updated_at']
    
    def validate(self, data):
        """Validaciones personalizadas"""
        flight = data.get('flight')
        
        # Verificar disponibilidad de asientos
        if flight and flight.available_seats <= 0:
            raise serializers.ValidationError(
                f"El vuelo {flight.flight_number} no tiene asientos disponibles"
            )
        
        return data


class BookingListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listado de reservas"""
    total_passengers = serializers.ReadOnlyField()
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'id', 'booking_number', 'user', 'user_name',
            'passenger_name', 'passenger_email', 'status',
            'total_passengers', 'total',
            'created_at', 'confirmed_at'
        ]


class BookingDetailFullSerializer(serializers.ModelSerializer):
    """Serializer completo para una reserva individual"""
    user_info = serializers.SerializerMethodField()
    passengers = BookingDetailSerializer(many=True, read_only=True)
    total_passengers = serializers.ReadOnlyField()
    
    class Meta:
        model = Booking
        fields = [
            'id', 'booking_number', 'user', 'user_info',
            'passenger_name', 'passenger_email', 'passenger_phone', 'passenger_document',
            'status', 'subtotal', 'tax', 'service_fee', 'total',
            'passengers', 'total_passengers',
            'created_at', 'updated_at', 'confirmed_at'
        ]
        read_only_fields = [
            'booking_number', 'subtotal', 'tax', 'service_fee', 'total',
            'created_at', 'updated_at', 'confirmed_at'
        ]
    
    def get_user_info(self, obj):
        return {
            'id': obj.user.id,
            'username': obj.user.username,
            'email': obj.user.email,
            'full_name': obj.user.get_full_name() or obj.user.username
        }


class BookingCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear una nueva reserva"""
    passengers = BookingDetailSerializer(many=True)
    
    class Meta:
        model = Booking
        fields = [
            'passenger_name', 'passenger_email', 'passenger_phone', 'passenger_document',
            'passengers'
        ]
    
    def create(self, validated_data):
        passengers_data = validated_data.pop('passengers')
        
        # Crear la reserva
        booking = Booking.objects.create(
            user=self.context['request'].user,
            **validated_data
        )
        
        # Crear los detalles de la reserva
        for passenger_data in passengers_data:
            flight = passenger_data['flight']
            
            # Verificar disponibilidad
            if flight.available_seats <= 0:
                booking.delete()
                raise serializers.ValidationError(
                    f"El vuelo {flight.flight_number} no tiene asientos disponibles"
                )
            
            # Crear el detalle
            BookingDetail.objects.create(
                booking=booking,
                **passenger_data
            )
            
            # Reducir asientos disponibles
            flight.available_seats -= 1
            flight.save(update_fields=['available_seats'])
        
        return booking
