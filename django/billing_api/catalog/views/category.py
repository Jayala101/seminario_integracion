# catalog/views/category.py
from rest_framework import viewsets, filters
from catalog.models import Category
from catalog.serializers import CategorySerializer
from catalog.permissions import IsAdminOrReadOnly

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ("name","slug")
    ordering_fields = ("name","created_at")
