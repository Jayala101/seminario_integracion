# catalog/views/product.py
from rest_framework import viewsets, filters
from catalog.models import Product
from catalog.serializers import ProductSerializer
from catalog.permissions import IsAdminOrReadOnly
from catalog.pagination import StandardResultsSetPagination

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related("category").all()
    serializer_class = ProductSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = StandardResultsSetPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ("name","slug","category__name")
    ordering_fields = ("price","created_at","name")

    def get_queryset(self):
        qs = super().get_queryset()
        category = self.request.query_params.get("category")
        is_active = self.request.query_params.get("is_active")
        if category:
            qs = qs.filter(category__id=category)
        if is_active is not None:
            qs = qs.filter(is_active=is_active.lower() in ("1","true","t","yes"))
        return qs
