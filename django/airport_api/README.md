# Airport Management API

API REST para gestión de aeropuertos construida con Django REST Framework. Sistema completo para administrar aerolíneas, aeropuertos, vuelos, pasajeros, reservas, tripulación y mantenimiento de aeronaves.

## Características

- **7 Entidades principales**: Airlines, Airports, Flights, Passengers, Bookings, Crew, Maintenance
- **Autenticación dual**: Token Authentication y JWT
- **Permisos por rol**: Usuario autenticado y Administrador
- **Base de datos**: PostgreSQL
- **Búsqueda y filtros** en todos los endpoints
- **Paginación automática** (20 items por página)
- **Documentación completa** con Postman Collection
- **Manejo de errores** centralizado
- **Logging** de operaciones

## Requisitos Previos

- Python 
- PostgreSQL 
- pip
- Virtualenv 

## Instalación

### 1. Clonar el repositorio

```bash
cd django/airport_api
```

### 2. Crear entorno virtual

```bash
python -m venv venv
```

### 3. Activar entorno virtual

**Windows:**
```bash
venv\Scripts\activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5. Configurar PostgreSQL

#### Crear base de datos

Abrir PostgreSQL con `psql` o pgAdmin y ejecutar:

```sql
CREATE DATABASE airport_db;
CREATE USER airport_user WITH PASSWORD 'admin';
ALTER ROLE airport_user SET client_encoding TO 'utf8';
ALTER ROLE airport_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE airport_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE airport_db TO airport_user;
```

### 6. Configurar variables de entorno

Crear archivo `.env` en la raíz del proyecto:

```env
# Django
SECRET_KEY=tu-clave-secreta-super-segura-aqui-cambiar-en-produccion
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL
DB_NAME=airport_db
DB_USER=airport_user
DB_PASS=admin
DB_HOST=localhost
DB_PORT=5432
```

### 7. Aplicar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 8. Crear superusuario

```bash
python manage.py createsuperuser
```

### 9. Ejecutar servidor

```bash
python manage.py runserver
```

El servidor estará disponible en: `http://localhost:8000`

## Endpoints Principales

### Autenticación

#### Token Authentication
```http
POST /api/auth/token/
Content-Type: application/json

{
    "username": "admin",
    "password": "admin"
}
```

**Respuesta:**
```json
{
    "token": "toke"
}
```

**Uso del token:**
```http
GET /api/airlines/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

#### JWT Authentication
```http
POST /api/auth/jwt/login/
Content-Type: application/json

{
    "username": "usuario",
    "password": "contraseña"
}
```

**Respuesta:**
```json
{
    "refresh": "token",
    "access": "token"
}
```

**Uso del JWT:**
```http
GET /api/airlines/
Authorization: Bearer {{token}}
```

**Renovar token:**
```http
POST /api/auth/jwt/refresh/
Content-Type: application/json

{
    "refresh": "token"
}
```

### Airlines (Aerolíneas)

```http
GET    /api/airlines/              # Listar todas
POST   /api/airlines/              # Crear (requiere auth)
GET    /api/airlines/{id}/         # Ver detalle
PUT    /api/airlines/{id}/         # Actualizar completo (requiere auth)
PATCH  /api/airlines/{id}/         # Actualizar parcial (requiere auth)
DELETE /api/airlines/{id}/         # Eliminar (requiere auth)

# Acciones adicionales
GET /api/airlines/by_country/?country=Colombia
GET /api/airlines/{id}/flights/
```

### Airports (Aeropuertos)

```http
GET    /api/airports/              # Listar todos
POST   /api/airports/              # Crear (requiere auth)
GET    /api/airports/{id}/         # Ver detalle
PUT    /api/airports/{id}/         # Actualizar (requiere auth)
DELETE /api/airports/{id}/         # Eliminar (requiere auth)

# Acciones adicionales
GET /api/airports/international/
GET /api/airports/{id}/departures/
GET /api/airports/{id}/arrivals/
```

### Flights (Vuelos)

```http
GET    /api/flights/               # Listar todos
POST   /api/flights/               # Crear (requiere auth)
GET    /api/flights/{id}/          # Ver detalle
PUT    /api/flights/{id}/          # Actualizar (requiere auth)
DELETE /api/flights/{id}/          # Eliminar (requiere auth)

# Acciones adicionales
GET  /api/flights/search/?origin=BOG&destination=MDE
GET  /api/flights/upcoming/
POST /api/flights/{id}/update_status/
```

### Passengers (Pasajeros)

```http
GET    /api/passengers/            # Listar todos
POST   /api/passengers/            # Crear (requiere auth)
GET    /api/passengers/{id}/       # Ver detalle
PUT    /api/passengers/{id}/       # Actualizar (requiere auth)
DELETE /api/passengers/{id}/       # Desactivar (requiere auth)

# Acciones adicionales
GET /api/passengers/{id}/bookings/
GET /api/passengers/frequent_flyers/
```

### Bookings (Reservas)

```http
GET    /api/bookings/              # Listar todas
POST   /api/bookings/              # Crear (requiere auth)
GET    /api/bookings/{id}/         # Ver detalle
PUT    /api/bookings/{id}/         # Actualizar (requiere auth)
DELETE /api/bookings/{id}/         # Cancelar (requiere auth)

# Acciones adicionales
POST /api/bookings/{id}/confirm/
POST /api/bookings/{id}/process_payment/
GET  /api/bookings/my_bookings/
```

### Crew (Tripulación)

```http
GET    /api/crew/members/          # Listar miembros
POST   /api/crew/members/          # Crear (requiere auth)
GET    /api/crew/members/{id}/     # Ver detalle
PUT    /api/crew/members/{id}/     # Actualizar (requiere auth)
DELETE /api/crew/members/{id}/     # Eliminar (requiere auth)

# Acciones adicionales
GET  /api/crew/members/available/
GET  /api/crew/members/by_role/?role=CAPTAIN
POST /api/crew/members/{id}/toggle_availability/

# Asignaciones
GET    /api/crew/assignments/      # Listar asignaciones
POST   /api/crew/assignments/      # Crear (requiere auth)
GET    /api/crew/assignments/by_flight/?flight_id=1
```

### Maintenance (Mantenimiento)

```http
# Aeronaves
GET    /api/maintenance/aircraft/  # Listar aeronaves
POST   /api/maintenance/aircraft/  # Crear (requiere auth)
GET    /api/maintenance/aircraft/{id}/
PUT    /api/maintenance/aircraft/{id}/
DELETE /api/maintenance/aircraft/{id}/

# Acciones adicionales
GET  /api/maintenance/aircraft/operational/
GET  /api/maintenance/aircraft/in_maintenance/
GET  /api/maintenance/aircraft/{id}/maintenance_history/
POST /api/maintenance/aircraft/{id}/update_status/

# Registros de mantenimiento
GET    /api/maintenance/records/   # Listar registros
POST   /api/maintenance/records/   # Crear (requiere auth)
GET    /api/maintenance/records/{id}/
PUT    /api/maintenance/records/{id}/
DELETE /api/maintenance/records/{id}/

# Acciones adicionales
GET  /api/maintenance/records/scheduled/
GET  /api/maintenance/records/in_progress/
GET  /api/maintenance/records/by_priority/?priority=HIGH
POST /api/maintenance/records/{id}/start_maintenance/
POST /api/maintenance/records/{id}/complete_maintenance/
```

## 🔍 Filtros, Búsqueda y Ordenamiento

### Filtros
```http
GET /api/flights/?status=SCHEDULED
GET /api/passengers/?nationality=Colombia
GET /api/crew/members/?role=CAPTAIN&status=ACTIVE
```

### Búsqueda
```http
GET /api/airlines/?search=avianca
GET /api/airports/?search=bogota
GET /api/passengers/?search=juan
```

### Ordenamiento
```http
GET /api/flights/?ordering=departure_time
GET /api/flights/?ordering=-departure_time  # Descendente
GET /api/bookings/?ordering=-booking_date
```

### Paginación
```http
GET /api/flights/?page=2
GET /api/flights/?page_size=50
```

## 🔐 Permisos

- **Lectura (GET)**: Público (sin autenticación)
- **Creación (POST)**: Requiere autenticación
- **Actualización (PUT/PATCH)**: Requiere autenticación
- **Eliminación (DELETE)**: Requiere autenticación

## 🛠️ Tecnologías Utilizadas

- **Django 4.2**: Framework web de Python
- **Django REST Framework**: Toolkit para construir Web APIs
- **PostgreSQL**: Base de datos relacional
- **djangorestframework-simplejwt**: Autenticación JWT
- **django-filter**: Filtrado de querysets
- **django-cors-headers**: Manejo de CORS
- **python-decouple**: Gestión de variables de entorno

## 📁 Estructura del Proyecto

```
airport_api/
├── manage.py
├── requirements.txt
├── README.md
├── .env
├── .env.example
├── .gitignore
├── airport_api/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── airlines/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── airports/
├── flights/
├── passengers/
├── bookings/
├── crew/
└── maintenance/
```

## 🐛 Manejo de Errores

La API retorna códigos HTTP estándar:

- `200 OK`: Operación exitosa
- `201 Created`: Recurso creado exitosamente
- `400 Bad Request`: Datos inválidos
- `401 Unauthorized`: No autenticado
- `403 Forbidden`: Sin permisos
- `404 Not Found`: Recurso no encontrado
- `500 Internal Server Error`: Error del servidor

Ejemplo de error:
```json
{
    "error": "No hay asientos disponibles en este vuelo"
}
```

## 📝 Postman Collection

Importar la colección `Airport_API.postman_collection.json` en Postman para probar todos los endpoints.

La colección incluye:
- Configuración de variables de entorno
- Ejemplos de todas las operaciones CRUD
- Autenticación Token y JWT
- Filtros y búsquedas
- Acciones personalizadas

## 🔄 Comandos Útiles

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Ejecutar tests
python manage.py test

# Shell interactivo
python manage.py shell

# Limpiar sesiones expiradas
python manage.py clearsessions
```

## 📊 Panel de Administración

Acceder a `http://localhost:8000/admin` con las credenciales del superusuario para gestionar todos los modelos mediante la interfaz de Django Admin.

## 🤝 Contribución

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📄 Licencia

Este proyecto es de uso educativo.

## ✉️ Contacto

Para consultas o soporte, contactar al equipo de desarrollo.

---

**Nota**: Este proyecto fue desarrollado como parte del Seminario de Integración.
