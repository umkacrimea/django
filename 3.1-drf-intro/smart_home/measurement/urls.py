from django.urls import path
from .views import SensorsListView, SensorDetailView, MeasurementCreateView

app_name = 'measurement'

urlpatterns = [
    # Датчики
    path('sensors/', SensorsListView.as_view(), name='sensors-list'),
    path('sensors/<int:pk>/', SensorDetailView.as_view(), name='sensor-detail'),
    
    # Измерения
    path('measurements/', MeasurementCreateView.as_view(), name='measurement-create'),
]