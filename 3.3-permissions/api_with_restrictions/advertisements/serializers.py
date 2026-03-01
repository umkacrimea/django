from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import serializers

from advertisements.models import Advertisement, AdvertisementStatusChoices


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""
    
    creator = UserSerializer(read_only=True)
    
    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator', 'status', 'created_at', 'updated_at')
        read_only_fields = ('creator', 'created_at', 'updated_at')

    def create(self, validated_data):
        """Создание объявления с автоматической простановкой создателя."""
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

    def validate(self, data):
        """Валидация: не больше 10 открытых объявлений у пользователя."""
        request = self.context.get('request')
        user = request.user if request else None
        
        # Пропускаем валидацию для админов (доп. задание)
        if user and user.is_staff:
            return data
        
        # Проверяем только при создании или смене статуса на OPEN
        is_creating = self.instance is None
        status_becomes_open = (
            data.get('status') == AdvertisementStatusChoices.OPEN or
            (self.instance and self.instance.status != AdvertisementStatusChoices.OPEN and 
             data.get('status') == AdvertisementStatusChoices.OPEN)
        )
        
        if user and (is_creating or status_becomes_open):
            # Считаем открытые объявления, исключая текущее при обновлении
            open_count = Advertisement.objects.filter(
                creator=user,
                status=AdvertisementStatusChoices.OPEN
            )
            if self.instance:
                open_count = open_count.exclude(pk=self.instance.pk)
            
            if open_count.count() >= 10:
                raise ValidationError('У вас не может быть больше 10 открытых объявлений')
        
        return data