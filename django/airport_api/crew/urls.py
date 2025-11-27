from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CrewMemberViewSet, FlightCrewAssignmentViewSet

router = DefaultRouter()
router.register(r'members', CrewMemberViewSet, basename='crew-member')
router.register(r'assignments', FlightCrewAssignmentViewSet, basename='crew-assignment')

urlpatterns = [
    path('', include(router.urls)),
]
