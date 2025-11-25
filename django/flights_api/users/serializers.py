from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer para el perfil de usuario"""
    class Meta:
        model = UserProfile
        fields = [
            'phone', 'date_of_birth', 'nationality',
            'document_type', 'document_number', 'document_expiry',
            'address', 'city', 'country', 'postal_code',
            'frequent_flyer_number', 'preferred_seat',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    """Serializer para el modelo User"""
    profile = UserProfileSerializer(required=False)
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'full_name', 'profile', 'date_joined', 'is_active'
        ]
        read_only_fields = ['date_joined']
    
    def get_full_name(self, obj):
        return obj.get_full_name() or obj.username
    
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        
        # Actualizar usuario
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Actualizar o crear perfil
        if profile_data:
            profile, created = UserProfile.objects.get_or_create(user=instance)
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()
        
        return instance


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer para registro de nuevos usuarios"""
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    profile = UserProfileSerializer(required=False)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password2',
            'first_name', 'last_name', 'profile'
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                "password": "Las contraseñas no coinciden"
            })
        
        if User.objects.filter(email=attrs.get('email')).exists():
            raise serializers.ValidationError({
                "email": "Este email ya está registrado"
            })
        
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        profile_data = validated_data.pop('profile', {})
        
        # Crear usuario
        user = User.objects.create_user(**validated_data)
        
        # Crear perfil
        if profile_data:
            UserProfile.objects.create(user=user, **profile_data)
        else:
            UserProfile.objects.create(user=user)
        
        return user


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer para cambio de contraseña"""
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password]
    )
    new_password2 = serializers.CharField(required=True, write_only=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({
                "new_password": "Las contraseñas nuevas no coinciden"
            })
        return attrs
