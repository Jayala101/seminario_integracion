from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """
    Permiso personalizado para permitir solo a administradores
    """
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            hasattr(request.user, 'profile') and
            request.user.profile.is_admin
        )


class IsAdminOrStaff(permissions.BasePermission):
    """
    Permiso para administradores y personal
    """
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            hasattr(request.user, 'profile') and
            request.user.profile.is_staff_member
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permiso que permite lectura a todos pero escritura solo a admin
    """
    def has_permission(self, request, view):
        # Permitir lectura a todos los autenticados
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # Escritura solo para admins
        return (
            request.user and
            request.user.is_authenticated and
            hasattr(request.user, 'profile') and
            request.user.profile.is_admin
        )


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permiso que permite al dueño del objeto o a admin
    """
    def has_object_permission(self, request, view, obj):
        # Admin puede hacer todo
        if hasattr(request.user, 'profile') and request.user.profile.is_admin:
            return True
        
        # El dueño puede ver y editar su objeto
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        return False
