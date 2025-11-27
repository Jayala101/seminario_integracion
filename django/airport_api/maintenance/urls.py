from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AircraftViewSet, MaintenanceRecordViewSet

router = DefaultRouter()
router.register(r'aircraft', AircraftViewSet, basename='aircraft')
router.register(r'records', MaintenanceRecordViewSet, basename='maintenance-record')

urlpatterns = [
    path('', include(router.urls)),
]
