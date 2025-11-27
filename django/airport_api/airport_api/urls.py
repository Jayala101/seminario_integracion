from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/token/', obtain_auth_token, name='api_token_auth'),
    path('api/auth/jwt/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/', include('rest_framework.urls')),
    path('api/airlines/', include('airlines.urls')),
    path('api/airports/', include('airports.urls')),
    path('api/flights/', include('flights.urls')),
    path('api/passengers/', include('passengers.urls')),
    path('api/bookings/', include('bookings.urls')),
    path('api/crew/', include('crew.urls')),
    path('api/maintenance/', include('maintenance.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = "Airport API - Administración"
admin.site.site_title = "Airport API"
admin.site.index_title = "Sistema de Gestión de Aeropuerto"
