#billing_api/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include('catalog.urls')), 
<<<<<<< HEAD
    path('api/', include('invoices.urls')), 
=======
    path('api/', include('invoices.urls')),
>>>>>>> ab7a16d92c366da0755c358a0b4f9e64d59831d1
]