from rest_framework import serializers
from .models import Sensor, Measurement


class MeasurementSerializer(serializers.ModelSerializer):
    """Сериализатор для создания измерения"""
    class Meta:
        model = Measurement
        fields = ['sensor', 'temperature', 'created_at', 'image']
        read_only_fields = ['created_at']  # время проставляется автоматически


class SensorSerializer(serializers.ModelSerializer):
    """Краткий сериализатор для списка датчиков"""
    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description']


class SensorDetailSerializer(serializers.ModelSerializer):
    """Подробный сериализатор датчика с вложенными измерениями"""
    measurements = MeasurementSerializer(read_only=True, many=True)

    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description', 'measurements']