from rest_framework.permissions import IsAuthenticated, AllowAny, BasePermission
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError  # ← импортируем

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement, AdvertisementStatusChoices  # ← импортируем Choices
from advertisements.serializers import AdvertisementSerializer


class IsAuthorOrAdmin(BasePermission):
    """Разрешает изменение/удаление только автору или админу."""
    
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return obj.creator == request.user or (request.user and request.user.is_staff)


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filterset_class = AdvertisementFilter
    
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    
    def get_permissions(self):
        action = self.action
        if action == 'create':
            return [IsAuthenticated()]
        if action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAuthorOrAdmin()]
        return [AllowAny()]
    
    def perform_create(self, serializer):
        """Создание с валидацией лимита открытых объявлений."""
        user = self.request.user
        status = self.request.data.get('status', AdvertisementStatusChoices.OPEN)
        
        # 🔹 Валидация: не больше 10 OPEN (кроме админов)
        if status == AdvertisementStatusChoices.OPEN and not user.is_staff:
            open_count = Advertisement.objects.filter(
                creator=user,
                status=AdvertisementStatusChoices.OPEN
            ).count()
            
            if open_count >= 10:
                raise ValidationError({'status': 'У вас не может быть больше 10 открытых объявлений'})
        
        # Сохраняем с автоматической простановкой creator
        serializer.save(creator=user)
    
    def perform_update(self, serializer):
        """Обновление с валидацией лимита при смене статуса на OPEN."""
        user = self.request.user
        old_status = serializer.instance.status
        new_status = self.request.data.get('status', old_status)
        
        # 🔹 Если меняем статус на OPEN — проверяем лимит
        if (old_status != AdvertisementStatusChoices.OPEN and 
            new_status == AdvertisementStatusChoices.OPEN and 
            not user.is_staff):
            
            # Считаем OPEN, исключая текущее объявление
            open_count = Advertisement.objects.filter(
                creator=user,
                status=AdvertisementStatusChoices.OPEN
            ).exclude(pk=serializer.instance.pk).count()
            
            if open_count >= 10:
                raise ValidationError({'status': 'У вас не может быть больше 10 открытых объявлений'})
        
        serializer.save()