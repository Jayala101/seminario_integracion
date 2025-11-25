from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .models import Booking, BookingDetail
from .serializers import (
    BookingListSerializer,
    BookingDetailFullSerializer,
    BookingCreateSerializer,
    BookingDetailSerializer
)


class BookingViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar reservas de vuelos.
    
    list: Retorna todas las reservas del usuario autenticado
    retrieve: Retorna una reserva específica
    create: Crea una nueva reserva
    update: Actualiza una reserva
    destroy: Elimina/Cancela una reserva
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['booking_number', 'passenger_name', 'passenger_email']
    ordering_fields = ['created_at', 'total']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Los usuarios solo ven sus propias reservas, admin ve todas"""
        if self.request.user.is_staff:
            return Booking.objects.all()
        return Booking.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return BookingCreateSerializer
        elif self.action == 'list':
            return BookingListSerializer
        return BookingDetailFullSerializer
    
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """Confirma una reserva"""
        booking = self.get_object()
        
        if booking.status != 'PENDING':
            return Response(
                {'error': 'Solo se pueden confirmar reservas pendientes'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        booking.status = 'CONFIRMED'
        booking.confirmed_at = timezone.now()
        booking.save()
        
        serializer = self.get_serializer(booking)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancela una reserva y libera los asientos"""
        booking = self.get_object()
        
        if booking.status == 'CANCELLED':
            return Response(
                {'error': 'Esta reserva ya está cancelada'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if booking.status == 'COMPLETED':
            return Response(
                {'error': 'No se pueden cancelar reservas completadas'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Liberar asientos
        for passenger in booking.passengers.all():
            flight = passenger.flight
            flight.available_seats += 1
            flight.save(update_fields=['available_seats'])
        
        booking.status = 'CANCELLED'
        booking.save()
        
        serializer = self.get_serializer(booking)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my_bookings(self, request):
        """Retorna todas las reservas del usuario actual"""
        bookings = self.get_queryset().filter(user=request.user)
        serializer = BookingListSerializer(bookings, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Retorna reservas próximas (confirmadas con vuelos futuros)"""
        now = timezone.now()
        bookings = self.get_queryset().filter(
            status='CONFIRMED',
            passengers__flight__departure_time__gte=now
        ).distinct()
        
        serializer = BookingListSerializer(bookings, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_passenger(self, request, pk=None):
        """Agrega un pasajero adicional a una reserva existente"""
        booking = self.get_object()
        
        if booking.status != 'PENDING':
            return Response(
                {'error': 'Solo se pueden agregar pasajeros a reservas pendientes'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = BookingDetailSerializer(data=request.data)
        if serializer.is_valid():
            flight = serializer.validated_data['flight']
            
            # Verificar disponibilidad
            if flight.available_seats <= 0:
                return Response(
                    {'error': f'El vuelo {flight.flight_number} no tiene asientos disponibles'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Crear el detalle
            serializer.save(booking=booking)
            
            # Reducir asientos
            flight.available_seats -= 1
            flight.save(update_fields=['available_seats'])
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
