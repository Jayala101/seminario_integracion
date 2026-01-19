from rest_framework import serializers
from .models import Passenger, UserProfile
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer para el perfil de usuario"""
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'phone', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    """Serializer para el modelo User con perfil"""
    profile = UserProfileSerializer(read_only=True)
    passenger_id = serializers.SerializerMethodField()
    role = serializers.CharField(write_only=True, required=False)
    phone = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False, min_length=8)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'role', 'phone', 'profile', 'passenger_id', 'is_active', 'date_joined', 'last_login']
        read_only_fields = ['date_joined', 'last_login']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def validate_password(self, value):
        """Validar password solo si se está creando o si se proporciona"""
        if self.instance is None and not value:
            raise serializers.ValidationError("La contraseña es requerida al crear un usuario")
        return value
    
    def get_passenger_id(self, obj):
        """Obtener el ID del pasajero asociado al usuario"""
        if hasattr(obj, 'passenger_profile'):
            return obj.passenger_profile.id
        return None
    
    def create(self, validated_data):
        role = validated_data.pop('role', 'CUSTOMER')
        phone = validated_data.pop('phone', '')
        password = validated_data.pop('password', None)
        
        if not password:
            raise serializers.ValidationError({'password': 'La contraseña es requerida'})
        
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        
        # Actualizar o crear perfil
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.role = role
        profile.phone = phone
        profile.save()
        
        return user
    
    def update(self, instance, validated_data):
        role = validated_data.pop('role', None)
        phone = validated_data.pop('phone', None)
        password = validated_data.pop('password', None)
        
        # Actualizar usuario
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        
        instance.save()
        
        # Actualizar perfil
        if hasattr(instance, 'profile'):
            if role:
                instance.profile.role = role
            if phone is not None:
                instance.profile.phone = phone
            instance.profile.save()
        
        return instance


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
