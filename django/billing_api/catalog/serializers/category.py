# catalog/serializers/category.py
from rest_framework import serializers
from catalog.models import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id","name","slug","created_at","updated_at")
        read_only_fields = ("id","created_at","updated_at")
