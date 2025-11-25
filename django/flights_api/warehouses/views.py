from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .models import Airport
from .serializers import AirportSerializer, AirportListSerializer


class AirportViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar aeropuertos.
    
    list: Retorna todos los aeropuertos
    retrieve: Retorna un aeropuerto específico
    create: Crea un nuevo aeropuerto
    update: Actualiza un aeropuerto
    destroy: Elimina un aeropuerto
    """
    queryset = Airport.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['country', 'city', 'is_international', 'is_active']
    search_fields = ['name', 'code', 'city', 'country']
    ordering_fields = ['name', 'code', 'city', 'country']
    ordering = ['name']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return AirportListSerializer
        return AirportSerializer
    
    @action(detail=True, methods=['get'])
    def departures(self, request, pk=None):
        """Obtiene todos los vuelos que salen de este aeropuerto"""
        from catalog.serializers import FlightListSerializer
        airport = self.get_object()
        flights = airport.departures.filter(
            is_active=True,
            departure_time__gte=timezone.now()
        ).order_by('departure_time')
        
        serializer = FlightListSerializer(flights, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def arrivals(self, request, pk=None):
        """Obtiene todos los vuelos que llegan a este aeropuerto"""
        from catalog.serializers import FlightListSerializer
        airport = self.get_object()
        flights = airport.arrivals.filter(
            is_active=True,
            arrival_time__gte=timezone.now()
        ).order_by('arrival_time')
        
        serializer = FlightListSerializer(flights, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def search_by_country(self, request):
        """Busca aeropuertos por país"""
        country = request.query_params.get('country')
        if not country:
            return Response(
                {'error': 'El parámetro country es requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        airports = self.get_queryset().filter(
            country__icontains=country,
            is_active=True
        )
        serializer = AirportListSerializer(airports, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def international(self, request):
        """Retorna solo aeropuertos internacionales"""
        airports = self.get_queryset().filter(
            is_international=True,
            is_active=True
        )
        serializer = AirportListSerializer(airports, many=True)
        return Response(serializer.data)
