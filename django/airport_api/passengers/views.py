from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from .models import Passenger, UserProfile
from .serializers import PassengerSerializer, UserSerializer, UserProfileSerializer
from .permissions import IsAdminUser, IsAdminOrStaff


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet para gestión de usuarios (solo admin)"""
    queryset = User.objects.all().select_related('profile')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['date_joined', 'username']
    ordering = ['-date_joined']
    
    def get_permissions(self):
        """Permitir registro público (POST) y me() para usuarios autenticados"""
        if self.action == 'create':
            return [AllowAny()]
        if self.action in ['me', 'retrieve', 'update', 'partial_update']:
            return [IsAuthenticated()]
        # Solo admin puede listar todos los usuarios o eliminar
        return [IsAdminUser()]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # Si no es admin, solo puede ver su propio usuario
        if not (hasattr(user, 'profile') and user.profile.is_admin):
            return queryset.filter(id=user.id)
        
        # Admin puede filtrar por rol
        role = self.request.query_params.get('role', None)
        if role:
            queryset = queryset.filter(profile__role=role)
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        return queryset
    
    def update(self, request, *args, **kwargs):
        """Permitir que usuarios editen solo su propia información"""
        instance = self.get_object()
        user = request.user
        
        # Verificar que el usuario solo edite su propia información o sea admin
        if instance.id != user.id and not (hasattr(user, 'profile') and user.profile.is_admin):
            return Response(
                {'error': 'No tiene permiso para editar este usuario'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        """Permitir que usuarios editen solo su propia información"""
        instance = self.get_object()
        user = request.user
        
        # Verificar que el usuario solo edite su propia información o sea admin
        if instance.id != user.id and not (hasattr(user, 'profile') and user.profile.is_admin):
            return Response(
                {'error': 'No tiene permiso para editar este usuario'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().partial_update(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Obtener información del usuario actual"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def change_role(self, request, pk=None):
        """Cambiar rol de un usuario"""
        user = self.get_object()
        new_role = request.data.get('role')
        
        if new_role not in ['ADMIN', 'STAFF', 'CUSTOMER']:
            return Response(
                {'error': 'Rol inválido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if hasattr(user, 'profile'):
            user.profile.role = new_role
            user.profile.save()
        else:
            UserProfile.objects.create(user=user, role=new_role)
        
        serializer = self.get_serializer(user)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        """Activar/desactivar usuario"""
        user = self.get_object()
        user.is_active = not user.is_active
        user.save()
        serializer = self.get_serializer(user)
        return Response(serializer.data)


class PassengerViewSet(viewsets.ModelViewSet):
    queryset = Passenger.objects.all()
    serializer_class = PassengerSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['nationality', 'document_type', 'is_active']
    search_fields = ['first_name', 'last_name', 'document_number', 'email']
    ordering_fields = ['last_name', 'first_name', 'created_at']
    ordering = ['last_name', 'first_name']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return super().get_permissions()
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            
            if instance.bookings.filter(status__in=['PENDING', 'CONFIRMED']).exists():
                return Response(
                    {'error': 'No se puede eliminar un pasajero con reservas activas'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            instance.is_active = False
            instance.save()
            
            return Response(
                {'message': 'Pasajero desactivado exitosamente'},
                status=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            return Response(
                {'error': f'Error al eliminar: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get'])
    def bookings(self, request, pk=None):
        passenger = self.get_object()
        bookings = passenger.bookings.all()
        
        from bookings.serializers import BookingSerializer
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def frequent_flyers(self, request):
        passengers = self.queryset.filter(
            frequent_flyer_number__isnull=False,
            is_active=True
        ).exclude(frequent_flyer_number='')
        
        serializer = self.get_serializer(passengers, many=True)
        return Response(serializer.data)
