from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Passenger, UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Perfil de Usuario'
    fk_name = 'user'


class CustomUserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_role')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    
    def get_role(self, obj):
        try:
            return obj.profile.get_role_display()
        except:
            return 'Sin perfil'
    get_role.short_description = 'Rol'


@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = [
        'full_name', 'document_number', 'email', 'nationality',
        'is_active', 'created_at'
    ]
    list_filter = ['is_active', 'document_type', 'nationality', 'gender']
    search_fields = ['first_name', 'last_name', 'document_number', 'email']
    ordering = ['last_name', 'first_name']
    list_per_page = 25
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('first_name', 'last_name', 'date_of_birth', 'nationality', 'gender')
        }),
        ('Documento de Identidad', {
            'fields': ('document_type', 'document_number', 'document_expiry')
        }),
        ('Contacto', {
            'fields': ('email', 'phone')
        }),
        ('Dirección', {
            'fields': ('address', 'city', 'country', 'postal_code')
        }),
        ('Preferencias', {
            'fields': ('frequent_flyer_number', 'special_needs')
        }),
        ('Sistema', {
            'fields': ('user', 'is_active')
        }),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone')


# Unregister the original User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
