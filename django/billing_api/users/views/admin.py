# users/serializers/admin.py
from django.contrib.auth.models import User
from rest_framework import serializers


# users/views/admin.py
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User
from users.serializers.admin import UserAdminListSerializer, UserAdminWriteSerializer

class UserAdminViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    permission_classes = (IsAdminUser,)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('username','email','first_name','last_name')
    ordering_fields = ('date_joined','username','email','last_login')

    def get_serializer_class(self):
        if self.action in ('list','retrieve'):
            return UserAdminListSerializer
        return UserAdminWriteSerializer

class UserAdminListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id','username','email','first_name','last_name',
            'is_active','is_staff','date_joined','last_login'
        )
        read_only_fields = ('id','date_joined','last_login')

class UserAdminWriteSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = (
            'username','email','first_name','last_name',
            'is_active','is_staff','password'
        )

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        user.set_password(password or User.objects.make_random_password())
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for k,v in validated_data.items():
            setattr(instance, k, v)
        if password:
            instance.set_password(password)
        instance.save()
        return instance