from rest_framework import serializers
from ..models import Warehouse

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['code', 'name', 'address', 'city', 'created_at', 'updated_at']
    
    def validate(self, value):
        if ' ' in value:
            raise serializers.ValidationError('code no debe contener espacios')
        return value
