from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Airline
from .serializers import AirlineSerializer


class AirlineViewSet(viewsets.ModelViewSet):
    queryset = Airline.objects.all()
    serializer_class = AirlineSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['country', 'is_active']
    search_fields = ['name', 'code', 'country', 'headquarters']
    ordering_fields = ['name', 'code', 'founded_year', 'fleet_size']
    ordering = ['name']
    
    def get_permissions(self):
        if self.action == 'destroy':
            return [IsAdminUser()]
        return super().get_permissions()
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            
            if instance.flights.filter(is_active=True).exists():
                return Response(
                    {'error': 'No se puede eliminar una aerolínea con vuelos activos'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            self.perform_destroy(instance)
            return Response(
                {'message': 'Aerolínea eliminada exitosamente'},
                status=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            return Response(
                {'error': f'Error al eliminar: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def by_country(self, request):
        country = request.query_params.get('country')
        if not country:
            return Response(
                {'error': 'El parámetro country es requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        airlines = self.queryset.filter(country__icontains=country, is_active=True)
        serializer = self.get_serializer(airlines, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def flights(self, request, pk=None):
        airline = self.get_object()
        flights = airline.flights.filter(is_active=True)
        
        from flights.serializers import FlightSerializer
        serializer = FlightSerializer(flights, many=True)
        return Response(serializer.data)
