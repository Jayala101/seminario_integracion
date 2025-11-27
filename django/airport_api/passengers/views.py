from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Passenger
from .serializers import PassengerSerializer


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
