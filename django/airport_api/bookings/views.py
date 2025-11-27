from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .models import Booking
from .serializers import BookingSerializer, BookingCreateSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.select_related('passenger', 'flight', 'flight__airline').all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'travel_class', 'flight', 'passenger']
    search_fields = ['booking_code', 'passenger__first_name', 'passenger__last_name']
    ordering_fields = ['booking_date', 'amount_paid', 'created_at']
    ordering = ['-booking_date']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return super().get_permissions()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return BookingCreateSerializer
        return BookingSerializer
    
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            booking = serializer.save()
            
            output_serializer = BookingSerializer(booking)
            return Response(
                output_serializer.data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {'error': f'Error al crear reserva: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            
            if instance.status == 'CANCELLED':
                return Response(
                    {'error': 'La reserva ya está cancelada'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if instance.status == 'COMPLETED':
                return Response(
                    {'error': 'No se puede cancelar una reserva completada'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            record.status = 'CANCELLED'
            instance.cancelled_at = timezone.now()
            instance.save()
            
            return Response(
                {'message': 'Reserva cancelada exitosamente'},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': f'Error al cancelar: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def confirm(self, request, pk=None):
        try:
            booking = self.get_object()
            
            if booking.status != 'PENDING':
                return Response(
                    {'error': 'Solo se pueden confirmar reservas pendientes'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            booking.status = 'CONFIRMED'
            booking.save()
            
            serializer = self.get_serializer(booking)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def process_payment(self, request, pk=None):
        try:
            booking = self.get_object()
            
            if booking.status not in ['PENDING', 'CONFIRMED']:
                return Response(
                    {'error': 'La reserva no está en estado válido para pago'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            amount = request.data.get('amount')
            payment_method = request.data.get('payment_method')
            
            if not amount or not payment_method:
                return Response(
                    {'error': 'Se requiere monto y método de pago'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            booking.amount_paid = amount
            booking.payment_method = payment_method
            booking.status = 'PAID'
            booking.save()
            
            serializer = self.get_serializer(booking)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def my_bookings(self, request):
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Autenticación requerida'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        try:
            passenger = request.user.passenger_profile
            bookings = self.queryset.filter(passenger=passenger)
            serializer = self.get_serializer(bookings, many=True)
            return Response(serializer.data)
        except:
            return Response([])
