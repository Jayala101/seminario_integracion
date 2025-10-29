# catalog/serializers/product.py
from rest_framework import serializers
from catalog.models import Product, Category

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source="category.name")
    category_id = serializers.PrimaryKeyRelatedField(
        source="category", queryset=Category.objects.all(), write_only=True
    )

    class Meta:
        model = Product
        fields = ("id","name","slug","price","stock","is_active",
                  "category_id","category_name","created_at","updated_at")
        read_only_fields = ("id","created_at","updated_at","category_name")
