from rest_framework import serializers
from .models import Passenger
from django.utils import timezone


class PassengerSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    bookings_count = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    
    class Meta:
        model = Passenger
        fields = [
            'id', 'user', 'first_name', 'last_name', 'full_name',
            'date_of_birth', 'age', 'nationality', 'gender',
            'document_type', 'document_number', 'document_expiry',
            'email', 'phone', 'address', 'city', 'country', 'postal_code',
            'frequent_flyer_number', 'special_needs', 'bookings_count',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
        extra_kwargs = {
            'document_number': {'write_only': False},
        }
    
    def get_bookings_count(self, obj):
        return obj.bookings.count()
    
    def get_age(self, obj):
        if not obj.date_of_birth:
            today = timezone.now().date()
            return today.year - obj.date_of_birth.year - (
                (today.month, today.day) < (obj.date_of_birth.month, obj.date_of_birth.day)
            )
        return None
    
    def validate_document_expiry(self, value):
        if value and value < timezone.now().date():
            raise serializers.ValidationError("El documento está vencido")
        return value
    
    def validate_email(self, value):
        if self.instance is None:
            if Passenger.objects.filter(email=value, is_active=True).exists():
                raise serializers.ValidationError("Ya existe un pasajero con este email")
        return value
