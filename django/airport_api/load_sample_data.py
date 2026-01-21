"""
Script para cargar datos de prueba en la base de datos del Airport API
Ejecutar desde el directorio django/airport_api/:
    python load_sample_data.py
O como manage.py:
    python manage.py shell < load_sample_data.py
"""

import os
import sys
import django
from datetime import datetime, timedelta
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'airport_api.settings')
django.setup()

from django.contrib.auth.models import User
from airlines.models import Airline
from airports.models import Airport
from flights.models import Flight
from passengers.models import Passenger, UserProfile
from bookings.models import Booking
from crew.models import CrewMember, FlightCrew
from maintenance.models import Aircraft, MaintenanceRecord


def create_users():
    """Crear usuarios de prueba"""
    print("Creando usuarios...")
    
    # Staff
    staff, created = User.objects.get_or_create(
        username='staff',
        defaults={
            'email': 'staff@airport.com',
            'first_name': 'Staff',
            'last_name': 'Member',
            'is_staff': True
        }
    )
    if created:
        staff.set_password('staff123')
        staff.save()
        UserProfile.objects.filter(user=staff).update(role='STAFF')
        print(f"  ✓ Usuario staff creado")
    
    # Clientes
    customers_data = [
        ('juan.perez', 'Juan', 'Pérez', 'juan.perez@email.com'),
        ('maria.garcia', 'María', 'García', 'maria.garcia@email.com'),
        ('carlos.lopez', 'Carlos', 'López', 'carlos.lopez@email.com'),
    ]
    
    for username, first_name, last_name, email in customers_data:
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'first_name': first_name,
                'last_name': last_name
            }
        )
        if created:
            user.set_password('customer123')
            user.save()
            print(f"  ✓ Usuario {username} creado")
    
    print(f"Total usuarios: {User.objects.count()}")


def create_airlines():
    """Crear aerolíneas"""
    print("\nCreando aerolíneas...")
    
    airlines_data = [
        {
            'code': 'AM',
            'name': 'Aeroméxico',
            'country': 'México',
            'founded_year': 1934,
            'fleet_size': 130,
            'headquarters': 'Ciudad de México',
            'website': 'https://www.aeromexico.com',
        },
        {
            'code': 'VB',
            'name': 'VivaAerobus',
            'country': 'México',
            'founded_year': 2006,
            'fleet_size': 50,
            'headquarters': 'Monterrey',
            'website': 'https://www.vivaaerobus.com',
        },
        {
            'code': 'Y4',
            'name': 'Volaris',
            'country': 'México',
            'founded_year': 2005,
            'fleet_size': 80,
            'headquarters': 'Ciudad de México',
            'website': 'https://www.volaris.com',
        },
        {
            'code': 'AA',
            'name': 'American Airlines',
            'country': 'Estados Unidos',
            'founded_year': 1926,
            'fleet_size': 900,
            'headquarters': 'Fort Worth, Texas',
            'website': 'https://www.aa.com',
        },
        {
            'code': 'DL',
            'name': 'Delta Air Lines',
            'country': 'Estados Unidos',
            'founded_year': 1924,
            'fleet_size': 900,
            'headquarters': 'Atlanta, Georgia',
            'website': 'https://www.delta.com',
        },
    ]
    
    for data in airlines_data:
        airline, created = Airline.objects.get_or_create(
            code=data['code'],
            defaults=data
        )
        if created:
            print(f"  ✓ Aerolínea {airline.code} - {airline.name} creada")
    
    print(f"Total aerolíneas: {Airline.objects.count()}")


def create_airports():
    """Crear aeropuertos"""
    print("\nCreando aeropuertos...")
    
    airports_data = [
        {
            'code': 'MEX',
            'name': 'Aeropuerto Internacional de la Ciudad de México',
            'city': 'Ciudad de México',
            'country': 'México',
            'latitude': Decimal('19.4363'),
            'longitude': Decimal('-99.0721'),
            'elevation': 2230,
            'timezone': 'America/Mexico_City',
            'terminals': 2,
            'runways': 2,
            'annual_passengers': 50000000,
        },
        {
            'code': 'GDL',
            'name': 'Aeropuerto Internacional de Guadalajara',
            'city': 'Guadalajara',
            'country': 'México',
            'latitude': Decimal('20.5218'),
            'longitude': Decimal('-103.3117'),
            'elevation': 1527,
            'timezone': 'America/Mexico_City',
            'terminals': 2,
            'runways': 2,
            'annual_passengers': 15000000,
        },
        {
            'code': 'MTY',
            'name': 'Aeropuerto Internacional de Monterrey',
            'city': 'Monterrey',
            'country': 'México',
            'latitude': Decimal('25.7785'),
            'longitude': Decimal('-100.1069'),
            'elevation': 387,
            'timezone': 'America/Monterrey',
            'terminals': 3,
            'runways': 2,
            'annual_passengers': 12000000,
        },
        {
            'code': 'CUN',
            'name': 'Aeropuerto Internacional de Cancún',
            'city': 'Cancún',
            'country': 'México',
            'latitude': Decimal('21.0365'),
            'longitude': Decimal('-86.8770'),
            'elevation': 7,
            'timezone': 'America/Cancun',
            'terminals': 4,
            'runways': 3,
            'annual_passengers': 25000000,
        },
        {
            'code': 'JFK',
            'name': 'John F. Kennedy International Airport',
            'city': 'New York',
            'country': 'Estados Unidos',
            'latitude': Decimal('40.6413'),
            'longitude': Decimal('-73.7781'),
            'elevation': 4,
            'timezone': 'America/New_York',
            'terminals': 6,
            'runways': 4,
            'annual_passengers': 62000000,
        },
        {
            'code': 'LAX',
            'name': 'Los Angeles International Airport',
            'city': 'Los Angeles',
            'country': 'Estados Unidos',
            'latitude': Decimal('33.9416'),
            'longitude': Decimal('-118.4085'),
            'elevation': 38,
            'timezone': 'America/Los_Angeles',
            'terminals': 9,
            'runways': 4,
            'annual_passengers': 88000000,
        },
    ]
    
    for data in airports_data:
        airport, created = Airport.objects.get_or_create(
            code=data['code'],
            defaults=data
        )
        if created:
            print(f"  ✓ Aeropuerto {airport.code} - {airport.name} creado")
    
    print(f"Total aeropuertos: {Airport.objects.count()}")


def create_flights():
    """Crear vuelos"""
    print("\nCreando vuelos...")
    
    airlines = list(Airline.objects.all())
    airports = list(Airport.objects.all())
    
    if not airlines or not airports:
        print("  ⚠ No hay aerolíneas o aeropuertos para crear vuelos")
        return
    
    # Crear vuelos para los próximos 7 días
    base_date = datetime.now()
    
    flights_data = [
        # Vuelos nacionales México
        ('MEX', 'GDL', 'AM', '100', 'Boeing 737', 8, 10, 150, 1500.00),
        ('MEX', 'MTY', 'VB', '200', 'Airbus A320', 7, 9, 180, 1200.00),
        ('MEX', 'CUN', 'Y4', '300', 'Airbus A320', 10, 13, 180, 2500.00),
        ('GDL', 'MEX', 'AM', '101', 'Boeing 737', 14, 16, 150, 1500.00),
        ('MTY', 'MEX', 'VB', '201', 'Airbus A320', 12, 14, 180, 1200.00),
        ('CUN', 'MEX', 'Y4', '301', 'Airbus A320', 16, 19, 180, 2500.00),
        
        # Vuelos internacionales
        ('MEX', 'JFK', 'AA', '400', 'Boeing 787', 6, 13, 250, 8500.00),
        ('MEX', 'LAX', 'DL', '500', 'Boeing 777', 8, 12, 300, 7000.00),
        ('JFK', 'MEX', 'AA', '401', 'Boeing 787', 14, 21, 250, 8500.00),
        ('LAX', 'MEX', 'DL', '501', 'Boeing 777', 18, 22, 300, 7000.00),
    ]
    
    created_count = 0
    for day in range(7):
        flight_date = base_date + timedelta(days=day)
        
        for origin_code, dest_code, airline_code, flight_num, aircraft, dep_hour, arr_hour, seats, price in flights_data:
            try:
                origin = Airport.objects.get(code=origin_code)
                destination = Airport.objects.get(code=dest_code)
                airline = Airline.objects.get(code=airline_code)
                
                departure = flight_date.replace(hour=dep_hour, minute=0, second=0, microsecond=0)
                arrival = flight_date.replace(hour=arr_hour, minute=30, second=0, microsecond=0)
                
                flight, created = Flight.objects.get_or_create(
                    airline=airline,
                    flight_number=f"{airline_code}{flight_num}",
                    departure_time=departure,
                    defaults={
                        'origin_airport': origin,
                        'destination_airport': destination,
                        'aircraft_type': aircraft,
                        'arrival_time': arrival,
                        'total_seats': seats,
                        'available_seats': seats,
                        'base_price': Decimal(str(price)),
                        'status': 'SCHEDULED',
                    }
                )
                
                if created:
                    created_count += 1
                    
            except Exception as e:
                print(f"  ⚠ Error creando vuelo {airline_code}{flight_num}: {e}")
    
    print(f"  ✓ {created_count} vuelos creados")
    print(f"Total vuelos: {Flight.objects.count()}")


def create_passengers():
    """Crear pasajeros adicionales"""
    print("\nCreando pasajeros...")
    
    passengers_data = [
        {
            'first_name': 'Ana',
            'last_name': 'Martínez',
            'date_of_birth': '1990-05-15',
            'nationality': 'México',
            'document_type': 'PASSPORT',
            'document_number': 'M12345678',
            'email': 'ana.martinez@email.com',
            'phone': '+5215551234567',
        },
        {
            'first_name': 'Roberto',
            'last_name': 'Hernández',
            'date_of_birth': '1985-08-22',
            'nationality': 'México',
            'document_type': 'ID_CARD',
            'document_number': 'HERR850822',
            'email': 'roberto.hernandez@email.com',
            'phone': '+5215557654321',
        },
        {
            'first_name': 'Laura',
            'last_name': 'González',
            'date_of_birth': '1995-12-10',
            'nationality': 'México',
            'document_type': 'PASSPORT',
            'document_number': 'M87654321',
            'email': 'laura.gonzalez@email.com',
            'phone': '+5215559876543',
        },
    ]
    
    created_count = 0
    for data in passengers_data:
        passenger, created = Passenger.objects.get_or_create(
            document_number=data['document_number'],
            defaults=data
        )
        if created:
            created_count += 1
            print(f"  ✓ Pasajero {passenger.first_name} {passenger.last_name} creado")
    
    print(f"Total pasajeros: {Passenger.objects.count()}")


def create_crew_members():
    """Crear tripulación"""
    print("\nCreando miembros de tripulación...")
    
    crew_data = [
        {
            'employee_id': 'CAP001',
            'first_name': 'Jorge',
            'last_name': 'Ramírez',
            'date_of_birth': '1975-03-15',
            'nationality': 'México',
            'role': 'CAPTAIN',
            'license_number': 'ATP-MX-12345',
            'license_expiry': '2027-12-31',
            'hire_date': '2005-01-10',
            'years_of_experience': 20,
            'flight_hours': 15000,
            'email': 'jorge.ramirez@airline.com',
            'phone': '+5215551111111',
            'emergency_contact': 'María Ramírez',
            'emergency_phone': '+5215552222222',
            'languages': 'Español, Inglés',
        },
        {
            'employee_id': 'FO001',
            'first_name': 'Patricia',
            'last_name': 'Morales',
            'date_of_birth': '1988-07-22',
            'nationality': 'México',
            'role': 'FIRST_OFFICER',
            'license_number': 'CPL-MX-67890',
            'license_expiry': '2026-06-30',
            'hire_date': '2015-03-20',
            'years_of_experience': 10,
            'flight_hours': 5000,
            'email': 'patricia.morales@airline.com',
            'phone': '+5215553333333',
            'emergency_contact': 'Luis Morales',
            'emergency_phone': '+5215554444444',
            'languages': 'Español, Inglés, Francés',
        },
        {
            'employee_id': 'FA001',
            'first_name': 'Carmen',
            'last_name': 'Torres',
            'date_of_birth': '1992-11-05',
            'nationality': 'México',
            'role': 'FLIGHT_ATTENDANT',
            'license_number': 'FA-MX-11111',
            'license_expiry': '2026-12-31',
            'hire_date': '2018-05-15',
            'years_of_experience': 7,
            'flight_hours': 3500,
            'email': 'carmen.torres@airline.com',
            'phone': '+5215555555555',
            'emergency_contact': 'Pedro Torres',
            'emergency_phone': '+5215556666666',
            'languages': 'Español, Inglés',
        },
        {
            'employee_id': 'FA002',
            'first_name': 'Miguel',
            'last_name': 'Sánchez',
            'date_of_birth': '1990-04-18',
            'nationality': 'México',
            'role': 'PURSER',
            'license_number': 'FA-MX-22222',
            'license_expiry': '2027-06-30',
            'hire_date': '2016-08-01',
            'years_of_experience': 9,
            'flight_hours': 4200,
            'email': 'miguel.sanchez@airline.com',
            'phone': '+5215557777777',
            'emergency_contact': 'Rosa Sánchez',
            'emergency_phone': '+5215558888888',
            'languages': 'Español, Inglés, Portugués',
        },
    ]
    
    created_count = 0
    for data in crew_data:
        crew, created = CrewMember.objects.get_or_create(
            employee_id=data['employee_id'],
            defaults=data
        )
        if created:
            created_count += 1
            print(f"  ✓ Tripulante {crew.first_name} {crew.last_name} ({crew.get_role_display()}) creado")
    
    print(f"Total tripulantes: {CrewMember.objects.count()}")


def create_aircraft():
    """Crear aeronaves"""
    print("\nCreando aeronaves...")
    
    airlines = {
        'AM': Airline.objects.filter(code='AM').first(),
        'VB': Airline.objects.filter(code='VB').first(),
        'Y4': Airline.objects.filter(code='Y4').first(),
        'AA': Airline.objects.filter(code='AA').first(),
        'DL': Airline.objects.filter(code='DL').first(),
    }
    
    aircraft_data = [
        # Aeroméxico
        {
            'registration': 'XA-AMR',
            'airline': airlines['AM'],
            'manufacturer': 'Boeing',
            'model': 'Boeing 737-800',
            'year_manufactured': 2018,
            'total_seats': 160,
            'first_class_seats': 12,
            'business_class_seats': 18,
            'economy_class_seats': 130,
            'status': 'OPERATIONAL',
            'flight_hours': 12500,
            'total_flights': 3200,
            'last_maintenance': (datetime.now() - timedelta(days=30)).date(),
            'next_maintenance': (datetime.now() + timedelta(days=60)).date(),
        },
        {
            'registration': 'XA-AMX',
            'airline': airlines['AM'],
            'manufacturer': 'Boeing',
            'model': 'Boeing 787-9',
            'year_manufactured': 2020,
            'total_seats': 274,
            'first_class_seats': 32,
            'business_class_seats': 48,
            'economy_class_seats': 194,
            'status': 'OPERATIONAL',
            'flight_hours': 8500,
            'total_flights': 1800,
            'last_maintenance': (datetime.now() - timedelta(days=20)).date(),
            'next_maintenance': (datetime.now() + timedelta(days=70)).date(),
        },
        {
            'registration': 'XA-AMP',
            'airline': airlines['AM'],
            'manufacturer': 'Embraer',
            'model': 'E190',
            'year_manufactured': 2019,
            'total_seats': 100,
            'first_class_seats': 0,
            'business_class_seats': 12,
            'economy_class_seats': 88,
            'status': 'MAINTENANCE',
            'flight_hours': 6200,
            'total_flights': 2100,
            'last_maintenance': datetime.now().date(),
            'next_maintenance': (datetime.now() + timedelta(days=90)).date(),
        },
        # VivaAerobus
        {
            'registration': 'XA-VIV',
            'airline': airlines['VB'],
            'manufacturer': 'Airbus',
            'model': 'A320-200',
            'year_manufactured': 2017,
            'total_seats': 180,
            'first_class_seats': 0,
            'business_class_seats': 0,
            'economy_class_seats': 180,
            'status': 'OPERATIONAL',
            'flight_hours': 15000,
            'total_flights': 4500,
            'last_maintenance': (datetime.now() - timedelta(days=45)).date(),
            'next_maintenance': (datetime.now() + timedelta(days=45)).date(),
        },
        {
            'registration': 'XA-VAB',
            'airline': airlines['VB'],
            'manufacturer': 'Airbus',
            'model': 'A321neo',
            'year_manufactured': 2021,
            'total_seats': 220,
            'first_class_seats': 0,
            'business_class_seats': 0,
            'economy_class_seats': 220,
            'status': 'OPERATIONAL',
            'flight_hours': 4200,
            'total_flights': 1100,
            'last_maintenance': (datetime.now() - timedelta(days=15)).date(),
            'next_maintenance': (datetime.now() + timedelta(days=75)).date(),
        },
        # Volaris
        {
            'registration': 'XA-VOL',
            'airline': airlines['Y4'],
            'manufacturer': 'Airbus',
            'model': 'A320neo',
            'year_manufactured': 2019,
            'total_seats': 186,
            'first_class_seats': 0,
            'business_class_seats': 0,
            'economy_class_seats': 186,
            'status': 'OPERATIONAL',
            'flight_hours': 9800,
            'total_flights': 2800,
            'last_maintenance': (datetime.now() - timedelta(days=25)).date(),
            'next_maintenance': (datetime.now() + timedelta(days=65)).date(),
        },
        {
            'registration': 'XA-VLR',
            'airline': airlines['Y4'],
            'manufacturer': 'Airbus',
            'model': 'A321neo',
            'year_manufactured': 2022,
            'total_seats': 240,
            'first_class_seats': 0,
            'business_class_seats': 0,
            'economy_class_seats': 240,
            'status': 'OPERATIONAL',
            'flight_hours': 2500,
            'total_flights': 650,
            'last_maintenance': (datetime.now() - timedelta(days=10)).date(),
            'next_maintenance': (datetime.now() + timedelta(days=80)).date(),
        },
        # American Airlines
        {
            'registration': 'N123AA',
            'airline': airlines['AA'],
            'manufacturer': 'Boeing',
            'model': 'Boeing 787-8',
            'year_manufactured': 2016,
            'total_seats': 234,
            'first_class_seats': 20,
            'business_class_seats': 28,
            'economy_class_seats': 186,
            'status': 'OPERATIONAL',
            'flight_hours': 18500,
            'total_flights': 4200,
            'last_maintenance': (datetime.now() - timedelta(days=35)).date(),
            'next_maintenance': (datetime.now() + timedelta(days=55)).date(),
        },
        {
            'registration': 'N456AA',
            'airline': airlines['AA'],
            'manufacturer': 'Boeing',
            'model': 'Boeing 777-300ER',
            'year_manufactured': 2015,
            'total_seats': 304,
            'first_class_seats': 8,
            'business_class_seats': 52,
            'economy_class_seats': 244,
            'status': 'OPERATIONAL',
            'flight_hours': 22000,
            'total_flights': 5100,
            'last_maintenance': (datetime.now() - timedelta(days=40)).date(),
            'next_maintenance': (datetime.now() + timedelta(days=50)).date(),
        },
        # Delta
        {
            'registration': 'N789DL',
            'airline': airlines['DL'],
            'manufacturer': 'Airbus',
            'model': 'A350-900',
            'year_manufactured': 2020,
            'total_seats': 306,
            'first_class_seats': 32,
            'business_class_seats': 48,
            'economy_class_seats': 226,
            'status': 'OPERATIONAL',
            'flight_hours': 7800,
            'total_flights': 1650,
            'last_maintenance': (datetime.now() - timedelta(days=18)).date(),
            'next_maintenance': (datetime.now() + timedelta(days=72)).date(),
        },
        {
            'registration': 'N321DL',
            'airline': airlines['DL'],
            'manufacturer': 'Boeing',
            'model': 'Boeing 767-400',
            'year_manufactured': 2014,
            'total_seats': 245,
            'first_class_seats': 24,
            'business_class_seats': 32,
            'economy_class_seats': 189,
            'status': 'OPERATIONAL',
            'flight_hours': 25000,
            'total_flights': 6200,
            'last_maintenance': (datetime.now() - timedelta(days=50)).date(),
            'next_maintenance': (datetime.now() + timedelta(days=40)).date(),
        },
    ]
    
    created_count = 0
    for data in aircraft_data:
        if data['airline']:  # Solo crear si la aerolínea existe
            aircraft, created = Aircraft.objects.get_or_create(
                registration=data['registration'],
                defaults=data
            )
            if created:
                created_count += 1
                print(f"  ✓ Aeronave {aircraft.registration} - {aircraft.manufacturer} {aircraft.model} creada")
    
    print(f"Total aeronaves: {Aircraft.objects.count()}")


def create_maintenance_records():
    """Crear registros de mantenimiento"""
    print("\nCreando registros de mantenimiento...")
    
    aircrafts = Aircraft.objects.all()
    
    if not aircrafts.exists():
        print("  ⚠ No hay aeronaves para crear registros de mantenimiento")
        return
    
    maintenance_data = [
        # Mantenimiento rutinario completado
        {
            'maintenance_type': 'ROUTINE',
            'priority': 'MEDIUM',
            'status': 'COMPLETED',
            'title': 'Inspección A-Check Rutinaria',
            'description': 'Inspección visual completa, verificación de sistemas y revisión de documentación.',
            'findings': 'Todos los sistemas operando normalmente. Se detectó desgaste menor en frenos.',
            'actions_taken': 'Se realizó servicing de rutina, lubricación de tren de aterrizaje, reemplazo preventivo de frenos.',
            'technician': 'Carlos Méndez',
            'supervisor': 'Roberto Sánchez',
            'scheduled_date': (datetime.now() - timedelta(days=30)).date(),
            'start_date': (datetime.now() - timedelta(days=30)).date(),
            'completion_date': (datetime.now() - timedelta(days=29)).date(),
            'estimated_hours': Decimal('8.00'),
            'actual_hours': Decimal('8.50'),
            'cost': Decimal('15000.00'),
            'parts_used': 'Filtros de aceite (2), Pastillas de freno (4), Fluidos hidráulicos',
        },
        # Mantenimiento preventivo programado
        {
            'maintenance_type': 'PREVENTIVE',
            'priority': 'HIGH',
            'status': 'SCHEDULED',
            'title': 'Inspección B-Check Programada',
            'description': 'Inspección detallada de estructuras, sistemas y componentes críticos.',
            'findings': '',
            'actions_taken': '',
            'technician': 'Ana López',
            'supervisor': 'Jorge Ramírez',
            'scheduled_date': (datetime.now() + timedelta(days=15)).date(),
            'start_date': None,
            'completion_date': None,
            'estimated_hours': Decimal('24.00'),
            'actual_hours': None,
            'cost': None,
            'parts_used': '',
        },
        # Reparación correctiva en progreso
        {
            'maintenance_type': 'CORRECTIVE',
            'priority': 'CRITICAL',
            'status': 'IN_PROGRESS',
            'title': 'Reparación de Sistema de Presurización',
            'description': 'Falla detectada en válvula de presurización durante vuelo. Requiere reemplazo inmediato.',
            'findings': 'Válvula de presurización con desgaste excesivo, fuga detectada en sello principal.',
            'actions_taken': 'Reemplazo de válvula de presurización, verificación de sistema completo.',
            'technician': 'Miguel Torres',
            'supervisor': 'Patricia Morales',
            'scheduled_date': datetime.now().date(),
            'start_date': datetime.now().date(),
            'completion_date': None,
            'estimated_hours': Decimal('12.00'),
            'actual_hours': None,
            'cost': Decimal('45000.00'),
            'parts_used': 'Válvula de presurización (P/N: 7823-45), Sellos y empaques',
        },
        # Inspección completada
        {
            'maintenance_type': 'INSPECTION',
            'priority': 'HIGH',
            'status': 'COMPLETED',
            'title': 'Inspección de Turbinas',
            'description': 'Inspección boroscópica de turbinas después de alcanzar 5000 horas de vuelo.',
            'findings': 'Turbinas en condiciones normales, ligera acumulación de carbonilla detectada.',
            'actions_taken': 'Limpieza de turbinas, ajuste de tolerancias, verificación de rendimiento.',
            'technician': 'Luis Fernández',
            'supervisor': 'Carmen Torres',
            'scheduled_date': (datetime.now() - timedelta(days=10)).date(),
            'start_date': (datetime.now() - timedelta(days=10)).date(),
            'completion_date': (datetime.now() - timedelta(days=8)).date(),
            'estimated_hours': Decimal('16.00'),
            'actual_hours': Decimal('18.00'),
            'cost': Decimal('32000.00'),
            'parts_used': 'Kit de limpieza de turbinas, Medidores de tolerancia',
        },
        # Revisión general programada
        {
            'maintenance_type': 'OVERHAUL',
            'priority': 'HIGH',
            'status': 'SCHEDULED',
            'title': 'Revisión General C-Check',
            'description': 'Revisión general programada cada 18 meses. Inspección exhaustiva de toda la aeronave.',
            'findings': '',
            'actions_taken': '',
            'technician': 'Equipo de Mantenimiento Mayor',
            'supervisor': 'Roberto Sánchez',
            'scheduled_date': (datetime.now() + timedelta(days=45)).date(),
            'start_date': None,
            'completion_date': None,
            'estimated_hours': Decimal('120.00'),
            'actual_hours': None,
            'cost': None,
            'parts_used': '',
        },
        # Reparación completada
        {
            'maintenance_type': 'REPAIR',
            'priority': 'HIGH',
            'status': 'COMPLETED',
            'title': 'Reparación de Tren de Aterrizaje',
            'description': 'Reemplazo de componentes hidráulicos del tren de aterrizaje principal.',
            'findings': 'Fuga en sistema hidráulico, actuador con desgaste excesivo.',
            'actions_taken': 'Reemplazo de actuador hidráulico, reparación de líneas, pruebas funcionales.',
            'technician': 'Pedro Ramírez',
            'supervisor': 'Jorge Ramírez',
            'scheduled_date': (datetime.now() - timedelta(days=20)).date(),
            'start_date': (datetime.now() - timedelta(days=20)).date(),
            'completion_date': (datetime.now() - timedelta(days=18)).date(),
            'estimated_hours': Decimal('20.00'),
            'actual_hours': Decimal('22.00'),
            'cost': Decimal('65000.00'),
            'parts_used': 'Actuador hidráulico (P/N: LG-4456), Mangueras hidráulicas (3), Sellos',
        },
        # Inspección de bajo nivel
        {
            'maintenance_type': 'INSPECTION',
            'priority': 'LOW',
            'status': 'COMPLETED',
            'title': 'Inspección Pre-Vuelo Extendida',
            'description': 'Inspección detallada antes de vuelo de largo alcance.',
            'findings': 'Aeronave en condiciones óptimas para vuelo.',
            'actions_taken': 'Verificación de niveles de fluidos, inspección visual externa, prueba de sistemas.',
            'technician': 'María González',
            'supervisor': '',
            'scheduled_date': (datetime.now() - timedelta(days=5)).date(),
            'start_date': (datetime.now() - timedelta(days=5)).date(),
            'completion_date': (datetime.now() - timedelta(days=5)).date(),
            'estimated_hours': Decimal('2.00'),
            'actual_hours': Decimal('2.00'),
            'cost': Decimal('1500.00'),
            'parts_used': 'Aceite de motor (10L), Fluido hidráulico (5L)',
        },
        # Mantenimiento preventivo
        {
            'maintenance_type': 'PREVENTIVE',
            'priority': 'MEDIUM',
            'status': 'COMPLETED',
            'title': 'Actualización de Software de Aviónica',
            'description': 'Actualización de sistema de navegación y comunicaciones.',
            'findings': 'Software actualizado exitosamente, todos los sistemas funcionando correctamente.',
            'actions_taken': 'Instalación de actualizaciones, verificación de sistemas, pruebas de comunicación.',
            'technician': 'Ricardo Vega',
            'supervisor': 'Patricia Morales',
            'scheduled_date': (datetime.now() - timedelta(days=15)).date(),
            'start_date': (datetime.now() - timedelta(days=15)).date(),
            'completion_date': (datetime.now() - timedelta(days=14)).date(),
            'estimated_hours': Decimal('4.00'),
            'actual_hours': Decimal('5.00'),
            'cost': Decimal('8000.00'),
            'parts_used': 'Licencia de software, Cables de actualización',
        },
    ]
    
    created_count = 0
    for i, data in enumerate(maintenance_data):
        aircraft = aircrafts[i % len(aircrafts)]
        
        record, created = MaintenanceRecord.objects.get_or_create(
            aircraft=aircraft,
            title=data['title'],
            scheduled_date=data['scheduled_date'],
            defaults=data
        )
        
        if created:
            created_count += 1
            print(f"  ✓ Registro de mantenimiento para {aircraft.registration} creado")
    
    print(f"Total registros de mantenimiento: {MaintenanceRecord.objects.count()}")


def create_bookings():
    """Crear reservas de ejemplo"""
    print("\nCreando reservas...")
    
    flights = Flight.objects.filter(departure_time__gte=datetime.now())[:5]
    passengers = Passenger.objects.all()[:3]
    
    if not flights.exists() or not passengers.exists():
        print("  ⚠ No hay vuelos o pasajeros para crear reservas")
        return
    
    created_count = 0
    for i, flight in enumerate(flights):
        passenger = passengers[i % len(passengers)]
        
        # Verificar si ya existe una reserva para este pasajero y vuelo
        if Booking.objects.filter(passenger=passenger, flight=flight, status__in=['PENDING', 'CONFIRMED', 'PAID']).exists():
            continue
        
        booking = Booking.objects.create(
            passenger=passenger,
            flight=flight,
            travel_class='ECONOMY',
            checked_baggage=1,
            carry_on_baggage=1,
            status='CONFIRMED',
            payment_method='CREDIT_CARD',
            amount_paid=flight.base_price,
        )
        
        # Actualizar asientos disponibles
        flight.available_seats -= 1
        flight.save()
        
        created_count += 1
        print(f"  ✓ Reserva {booking.booking_code} creada para {passenger.first_name} en vuelo {flight.flight_number}")
    
    print(f"Total reservas: {Booking.objects.count()}")


def assign_crew_to_flights():
    """Asignar tripulación a vuelos"""
    print("\nAsignando tripulación a vuelos...")
    
    flights = Flight.objects.filter(departure_time__gte=datetime.now())[:5]
    captains = list(CrewMember.objects.filter(role='CAPTAIN'))
    first_officers = list(CrewMember.objects.filter(role='FIRST_OFFICER'))
    attendants = list(CrewMember.objects.filter(role__in=['FLIGHT_ATTENDANT', 'PURSER']))
    
    if not all([flights.exists(), captains, first_officers, attendants]):
        print("  ⚠ No hay suficiente tripulación o vuelos")
        return
    
    created_count = 0
    for i, flight in enumerate(flights):
        # Asignar capitán
        if captains:
            FlightCrew.objects.get_or_create(
                flight=flight,
                crew_member=captains[i % len(captains)],
                defaults={'role': 'CAPTAIN'}
            )
            created_count += 1
        
        # Asignar primer oficial
        if first_officers:
            FlightCrew.objects.get_or_create(
                flight=flight,
                crew_member=first_officers[i % len(first_officers)],
                defaults={'role': 'FIRST_OFFICER'}
            )
            created_count += 1
        
        # Asignar asistentes
        for j in range(min(2, len(attendants))):
            attendant = attendants[(i + j) % len(attendants)]
            FlightCrew.objects.get_or_create(
                flight=flight,
                crew_member=attendant,
                defaults={'role': attendant.role}
            )
            created_count += 1
    
    print(f"  ✓ {created_count} asignaciones de tripulación creadas")
    print(f"Total asignaciones: {FlightCrew.objects.count()}")


def main():
    """Función principal"""
    print("=" * 60)
    print("CARGANDO DATOS DE PRUEBA - AIRPORT API")
    print("=" * 60)
    
    try:
        create_users()
        create_airlines()
        create_airports()
        create_flights()
        create_passengers()
        create_crew_members()
        create_aircraft()
        create_maintenance_records()
        create_bookings()
        assign_crew_to_flights()
        
        print("\n" + "=" * 60)
        print("✓ DATOS CARGADOS EXITOSAMENTE")
        print("=" * 60)
        print("\nResumen:")
        print(f"  • Usuarios: {User.objects.count()}")
        print(f"  • Aerolíneas: {Airline.objects.count()}")
        print(f"  • Aeropuertos: {Airport.objects.count()}")
        print(f"  • Vuelos: {Flight.objects.count()}")
        print(f"  • Pasajeros: {Passenger.objects.count()}")
        print(f"  • Tripulantes: {CrewMember.objects.count()}")
        print(f"  • Aeronaves: {Aircraft.objects.count()}")
        print(f"  • Registros de mantenimiento: {MaintenanceRecord.objects.count()}")
        print(f"  • Reservas: {Booking.objects.count()}")
        print(f"  • Asignaciones de tripulación: {FlightCrew.objects.count()}")
        
        print("\n" + "=" * 60)
        print("CREDENCIALES DE ACCESO:")
        print("=" * 60)
        print("Staff:")
        print("  Usuario: staff")
        print("  Contraseña: staff123")
        print("\nClientes:")
        print("  Usuario: juan.perez / maria.garcia / carlos.lopez")
        print("  Contraseña: customer123")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n⚠ Error durante la carga de datos: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
