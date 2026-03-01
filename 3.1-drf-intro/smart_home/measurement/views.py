from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Sensor, Measurement
from .serializers import SensorSerializer, SensorDetailSerializer, MeasurementSerializer


class SensorsListView(generics.ListCreateAPIView):
    """
    GET: список всех датчиков (кратко)
    POST: создать новый датчик
    """
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class SensorDetailView(generics.RetrieveUpdateAPIView):
    """
    GET: детальная информация о датчике + все измерения
    PATCH/PUT: обновить название/описание датчика
    """
    queryset = Sensor.objects.all()
    serializer_class = SensorDetailSerializer


class MeasurementCreateView(generics.CreateAPIView):
    """
    POST: добавить новое измерение температуры
    """
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer

    def create(self, request, *args, **kwargs):
        """Переопределяем для возврата ID созданного измерения"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Возвращаем ID и время создания
        headers = self.get_success_headers(serializer.data)
        return Response(
            {'id': serializer.instance.id, 'created_at': serializer.instance.created_at},
            status=status.HTTP_201_CREATED,
            headers=headers
        )