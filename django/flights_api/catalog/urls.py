from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AirlineViewSet, FlightViewSet

router = DefaultRouter()
router.register(r'airlines', AirlineViewSet, basename='airline')
router.register(r'flights', FlightViewSet, basename='flight')

urlpatterns = [
    path('', include(router.urls)),
]
