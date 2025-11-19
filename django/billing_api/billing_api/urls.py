#billing_api/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include('catalog.urls')), 
    path('api/', include('invoices.urls')), 
    path('api/', include('warehouses.urls')), 
    path('api/', include('basics.urls')), 
]