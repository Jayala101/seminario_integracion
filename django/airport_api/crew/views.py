from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import CrewMember, FlightCrewAssignment
from .serializers import CrewMemberSerializer, FlightCrewAssignmentSerializer


class CrewMemberViewSet(viewsets.ModelViewSet):
    queryset = CrewMember.objects.all()
    serializer_class = CrewMemberSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['role', 'status', 'is_available', 'nationality']
    search_fields = ['employee_id', 'first_name', 'last_name', 'email']
    ordering_fields = ['last_name', 'first_name', 'hire_date', 'flight_hours']
    ordering = ['last_name', 'first_name']
    
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        if self.action == 'register':
            return [AllowAny()]
        if self.action == 'create':
            return [IsAuthenticated()]
        return super().get_permissions()
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        """
        Endpoint público para registro de nuevos tripulantes
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        crew = self.queryset.filter(status='ACTIVE', is_available=True)
        
        role = request.query_params.get('role')
        if role:
            crew = crew.filter(role=role)
        
        serializer = self.get_serializer(crew, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_role(self, request):
        role = request.query_params.get('role')
        if not role:
            return Response(
                {'error': 'Se requiere parámetro role'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        crew = self.queryset.filter(role=role, status='ACTIVE')
        serializer = self.get_serializer(crew, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def assignments(self, request, pk=None):
        member = self.get_object()
        assignments = crew_member.flight_assignments.all()
        
        serializer = FlightCrewAssignmentSerializer(assignments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def toggle_availability(self, request, pk=None):
        try:
            crew_member = self.get_object()
            crew_member.is_available = not crew_member.is_available
            crew_member.save()
            
            serializer = self.get_serializer(crew_member)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class FlightCrewAssignmentViewSet(viewsets.ModelViewSet):
    queryset = FlightCrewAssignment.objects.select_related('flight', 'crew_member').all()
    serializer_class = FlightCrewAssignmentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['flight', 'crew_member', 'crew_member__role']
    search_fields = ['crew_member__first_name', 'crew_member__last_name', 'flight__flight_number']
    ordering_fields = ['assigned_at', 'flight__departure_time']
    ordering = ['-assigned_at']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return super().get_permissions()
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_assignments(self, request):
        """
        Retorna las asignaciones de vuelo del crew member autenticado
        """
        try:
            # Buscar el crew member asociado al usuario autenticado por email
            crew_member = CrewMember.objects.get(email=request.user.email)
            
            # Obtener asignaciones del crew member con detalles del vuelo
            assignments = self.queryset.filter(crew_member=crew_member).select_related(
                'flight__origin_airport',
                'flight__destination_airport',
                'flight__airline'
            )
            
            # Serializar con detalles adicionales del vuelo
            data = []
            for assignment in assignments:
                flight = assignment.flight
                data.append({
                    'id': assignment.id,
                    'flight': flight.id,
                    'flight_number': flight.flight_number,
                    'crew_member': crew_member.id,
                    'crew_member_name': crew_member.full_name,
                    'crew_member_role': crew_member.get_role_display(),
                    'assigned_at': assignment.assigned_at,
                    'notes': assignment.notes,
                    'flight_details': {
                        'flight_number': flight.flight_number,
                        'origin_airport_name': flight.origin_airport.name if flight.origin_airport else 'N/A',
                        'destination_airport_name': flight.destination_airport.name if flight.destination_airport else 'N/A',
                        'departure_time': flight.departure_time,
                        'arrival_time': flight.arrival_time,
                        'status': flight.status,
                        'aircraft_type': flight.aircraft_type,
                        'gate': flight.gate,
                    }
                })
            
            return Response(data)
        except CrewMember.DoesNotExist:
            return Response(
                {'error': 'No se encontró un miembro de tripulación asociado a este usuario'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def by_flight(self, request):
        flight_id = request.query_params.get('flight_id')
        if not flight_id:
            return Response(
                {'error': 'Se requiere parámetro flight_id'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        assignments = self.queryset.filter(flight_id=flight_id)
        serializer = self.get_serializer(assignments, many=True)
        return Response(serializer.data)
