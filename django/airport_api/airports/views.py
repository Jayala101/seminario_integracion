from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from .models import Airport
from .serializers import AirportSerializer


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['country', 'city', 'is_international', 'is_cargo', 'is_active']
    search_fields = ['name', 'code', 'city', 'country']
    ordering_fields = ['name', 'code', 'city', 'annual_passengers']
    ordering = ['name']
    
    def get_permissions(self):
        if self.action == 'destroy':
            return [IsAdminUser()]
        return super().get_permissions()
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            
            if instance.departures.exists() or instance.arrivals.exists():
                return Response(
                    {'error': 'No se puede eliminar un aeropuerto con vuelos registrados'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            self.perform_destroy(instance)
            return Response(
                {'message': 'Aeropuerto eliminado exitosamente'},
                status=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            return Response(
                {'error': f'Error al eliminar: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def international(self, request):
        airports = self.queryset.filter(is_international=True, is_active=True)
        serializer = self.get_serializer(airports, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def departures(self, request, pk=None):
        airport = self.get_object()
        flights = airport.departures.filter(is_active=True)
        
        from flights.serializers import FlightSerializer
        serializer = FlightSerializer(flights, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def arrivals(self, request, pk=None):
        airport = self.get_object()
        flights = airport.arrivals.filter(is_active=True)
        
        from flights.serializers import FlightSerializer
        serializer = FlightSerializer(flights, many=True)
        return Response(serializer.data)
