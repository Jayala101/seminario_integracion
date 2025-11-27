from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from datetime import timedelta
from .models import Flight
from .serializers import FlightSerializer


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.select_related(
        'airline', 'origin_airport', 'destination_airport'
    ).all()
    serializer_class = FlightSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'airline', 'origin_airport', 'destination_airport',
        'flight_class', 'status', 'is_active'
    ]
    search_fields = ['flight_number', 'airline__name', 'aircraft_type']
    ordering_fields = ['departure_time', 'arrival_time', 'base_price']
    ordering = ['-departure_time']
    
    def get_permissions(self):
        if self.action == 'destroy':
            return [IsAdminUser()]
        return super().get_permissions()
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            
            if instance.bookings.exists():
                return Response(
                    {'error': 'No se puede eliminar un vuelo con reservas'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            self.perform_destroy(instance)
            return Response(
                {'message': 'Vuelo eliminado exitosamente'},
                status=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            return Response(
                {'error': f'Error al eliminar: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        origin = request.query_params.get('origin')
        destination = request.query_params.get('destination')
        date = request.query_params.get('date')
        
        queryset = self.get_queryset().filter(is_active=True, status='SCHEDULED')
        
        if origin:
            queryset = queryset.filter(origin_airport__code__iexact=origin)
        if destination:
            queryset = queryset.filter(destination_airport__code__iexact=destination)
        if date:
            queryset = queryset.filter(departure_time__date=date)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        now = timezone.now()
        next_week = now + timedelta(days=7)
        flights = self.get_queryset().filter(
            departure_time__gte=now,
            departure_time__lte=next_week,
            is_active=True
        )
        serializer = self.get_serializer(flights, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
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
