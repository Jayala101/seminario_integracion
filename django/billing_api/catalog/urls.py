# catalog/urls.py
from rest_framework.routers import DefaultRouter
from catalog.views.category import CategoryViewSet
from catalog.views.product import ProductViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = router.urls
