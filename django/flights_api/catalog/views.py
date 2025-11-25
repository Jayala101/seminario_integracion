from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from datetime import timedelta
from .models import Airline, Flight
from .serializers import (
    AirlineSerializer, 
    FlightListSerializer, 
    FlightDetailSerializer
)


class AirlineViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar aerolíneas.
    
    list: Retorna todas las aerolíneas
    retrieve: Retorna una aerolínea específica
    create: Crea una nueva aerolínea
    update: Actualiza una aerolínea
    destroy: Elimina una aerolínea
    """
    queryset = Airline.objects.all()
    serializer_class = AirlineSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['country', 'is_active']
    search_fields = ['name', 'code', 'country']
    ordering_fields = ['name', 'code', 'created_at']
    ordering = ['name']
    
    @action(detail=True, methods=['get'])
    def flights(self, request, pk=None):
        """Obtiene todos los vuelos de una aerolínea"""
        airline = self.get_object()
        flights = airline.flights.filter(is_active=True)
        serializer = FlightListSerializer(flights, many=True)
        return Response(serializer.data)


class FlightViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar vuelos.
    
    list: Retorna todos los vuelos
    retrieve: Retorna un vuelo específico
    create: Crea un nuevo vuelo
    update: Actualiza un vuelo
    destroy: Elimina un vuelo
    """
    queryset = Flight.objects.select_related(
        'airline', 'origin_airport', 'destination_airport'
    ).all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'airline', 'origin_airport', 'destination_airport',
        'flight_class', 'status', 'is_active'
    ]
    search_fields = ['flight_number', 'airline__name', 'airline__code']
    ordering_fields = ['departure_time', 'arrival_time', 'base_price']
    ordering = ['-departure_time']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return FlightListSerializer
        return FlightDetailSerializer
    
    @action(detail=False, methods=['get'])
    def search_flights(self, request):
        """
        Búsqueda avanzada de vuelos.
        Parámetros:
        - origin: Código del aeropuerto de origen
        - destination: Código del aeropuerto de destino
        - date: Fecha de salida (YYYY-MM-DD)
        - class: Clase del vuelo
        """
        origin = request.query_params.get('origin')
        destination = request.query_params.get('destination')
        date = request.query_params.get('date')
        flight_class = request.query_params.get('class')
        
        queryset = self.get_queryset().filter(is_active=True, status='SCHEDULED')
        
        if origin:
            queryset = queryset.filter(origin_airport__code__iexact=origin)
        if destination:
            queryset = queryset.filter(destination_airport__code__iexact=destination)
        if date:
            queryset = queryset.filter(departure_time__date=date)
        if flight_class:
            queryset = queryset.filter(flight_class=flight_class)
        
        serializer = FlightListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Retorna vuelos próximos (siguientes 7 días)"""
        now = timezone.now()
        next_week = now + timedelta(days=7)
        queryset = self.get_queryset().filter(
            departure_time__gte=now,
            departure_time__lte=next_week,
            is_active=True
        )
        serializer = FlightListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Actualiza el estado de un vuelo"""
        flight = self.get_object()
        new_status = request.data.get('status')
        
        if new_status not in dict(Flight.STATUS_CHOICES):
            return Response(
                {'error': 'Estado inválido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        flight.status = new_status
        flight.save()
        serializer = self.get_serializer(flight)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def availability(self, request, pk=None):
        """Verifica disponibilidad de asientos"""
        flight = self.get_object()
        return Response({
            'flight_id': flight.id,
            'flight_number': f"{flight.airline.code}{flight.flight_number}",
            'total_seats': flight.total_seats,
            'available_seats': flight.available_seats,
            'occupied_seats': flight.total_seats - flight.available_seats,
            'is_full': flight.is_full,
            'occupancy_percentage': flight.occupancy_percentage
        })
