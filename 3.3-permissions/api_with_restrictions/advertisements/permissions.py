from rest_framework import permissions
from advertisements.models import Advertisement


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Разрешает:
    - Чтение любому
    - Изменение/удаление только автору или админу
    """
    
    def has_object_permission(self, request, view, obj):
        # Чтение разрешено всем
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Изменение/удаление — только автору или админу
        return obj.creator == request.user or (request.user and request.user.is_staff)


class IsAuthorOrAdmin(permissions.BasePermission):
    """
    Разрешает создание только авторизованным пользователям.
    Для update/delete — только автор или админ.
    """
    
    def has_permission(self, request, view):
        # Создание — только авторизованным
        if view.action == 'create':
            return request.user and request.user.is_authenticated
        # Чтение — всем
        return True
    
    def has_object_permission(self, request, view, obj):
        # Чтение — всем
        if request.method in permissions.SAFE_METHODS:
            return True
        # Изменение/удаление — автору или админу
        return obj.creator == request.user or (request.user and request.user.is_staff)