from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .models import Aircraft, MaintenanceRecord
from .serializers import AircraftSerializer, MaintenanceRecordSerializer


class AircraftViewSet(viewsets.ModelViewSet):
    queryset = Aircraft.objects.select_related('airline').all()
    serializer_class = AircraftSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['airline', 'status', 'manufacturer', 'model']
    search_fields = ['registration', 'manufacturer', 'model']
    ordering_fields = ['registration', 'year_manufactured', 'flight_hours', 'total_flights']
    ordering = ['registration']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return super().get_permissions()
    
    @action(detail=False, methods=['get'])
    def operational(self, request):
        aircrafts = self.queryset.filter(status='OPERATIONAL')
        serializer = self.get_serializer(aircrafts, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def in_maintenance(self, request):
        aircrafts = self.queryset.filter(status='MAINTENANCE')
        serializer = self.get_serializer(aircrafts, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def maintenance_history(self, request, pk=None):
        aircraft = self.get_object()
        records = aircraft.maintenance_records.all()
        
        serializer = MaintenanceRecordSerializer(records, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def update_status(self, request, pk=None):
        try:
            aircraft = self.get_object()
            new_status = request.data.get('status')
            
            if not new_status:
                return Response(
                    {'error': 'Se requiere el campo status'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            valid_statuses = dict(Aircraft.STATUS_CHOICES).keys()
            if new_status not in valid_statuses:
                return Response(
                    {'error': f'Estado inválido. Opciones: {", ".join(valid_statuses)}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            aircraft.status = new_status
            aircraft.save()
            
            serializer = self.get_serializer(aircraft)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class MaintenanceRecordViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceRecord.objects.select_related('aircraft', 'aircraft__airline').all()
    serializer_class = MaintenanceRecordSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['aircraft', 'maintenance_type', 'priority', 'status']
    search_fields = ['title', 'description', 'technician', 'aircraft__registration']
    ordering_fields = ['scheduled_date', 'priority', 'created_at']
    ordering = ['-scheduled_date']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return super().get_permissions()
    
    @action(detail=False, methods=['get'])
    def scheduled(self, request):
        records = self.queryset.filter(status='SCHEDULED')
        serializer = self.get_serializer(records, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def in_progress(self, request):
        records = self.queryset.filter(status='IN_PROGRESS')
        serializer = self.get_serializer(records, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_priority(self, request):
        priority = request.query_params.get('priority')
        if not priority:
            return Response(
                {'error': 'Se requiere parámetro priority'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        records = self.queryset.filter(priority=priority, status__in=['SCHEDULED', 'IN_PROGRESS'])
        serializer = self.get_serializer(records, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def start_maintenance(self, request, pk=None):
        try:
            record = self.get_object()
            
            if record.status != 'SCHEDULED':
                return Response(
                    {'error': 'Solo se pueden iniciar mantenimientos programados'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            record.status = 'IN_PROGRESS'
            record.start_date = timezone.now().date()
            record.save()
            
            record.aircraft.status = 'MAINTENANCE'
            record.aircraft.save()
            
            serializer = self.get_serializer(record)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def complete_maintenance(self, request, pk=None):
        try:
            record = self.get_object()
            
            if record.status != 'IN_PROGRESS':
                return Response(
                    {'error': 'Solo se pueden completar mantenimientos en progreso'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            record.status = 'COMPLETED'
            record.completion_date = timezone.now().date()
            record.actual_hours = request.data.get('actual_hours', record.estimated_hours)
            record.cost = request.data.get('cost', 0)
            record.findings = request.data.get('findings', '')
            record.actions_taken = request.data.get('actions_taken', '')
            record.save()
            
            record.aircraft.last_maintenance = record.completion_date
            record.aircraft.status = 'OPERATIONAL'
            record.aircraft.save()
            
            serializer = self.get_serializer(record)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
