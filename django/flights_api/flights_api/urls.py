"""
URL configuration for flights_api project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/catalog/', include('catalog.urls')),
    path('api/airports/', include('warehouses.urls')),
    path('api/bookings/', include('invoices.urls')),
    path('api/users/', include('users.urls')),
]
