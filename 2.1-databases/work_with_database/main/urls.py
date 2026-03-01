from django.contrib import admin
from django.urls import path, include
from phones.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),  # корень сайта → редирект на каталог
    path('catalog/', include('phones.urls')),  # все маршруты каталога
]