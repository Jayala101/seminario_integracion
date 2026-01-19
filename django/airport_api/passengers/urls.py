from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PassengerViewSet, UserViewSet

router = DefaultRouter()
router.register(r'passengers', PassengerViewSet, basename='passenger')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]
