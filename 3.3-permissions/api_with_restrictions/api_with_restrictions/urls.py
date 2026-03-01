from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from advertisements.views import AdvertisementViewSet

# 🔹 Регистрируем ViewSet в роутере
router = DefaultRouter()
router.register('advertisements', AdvertisementViewSet, basename='advertisement')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # все маршруты под /api/
    path('api-auth/', include('rest_framework.urls')),  # login/logout для Browsable API
]