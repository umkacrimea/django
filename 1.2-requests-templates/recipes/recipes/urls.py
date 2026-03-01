from django.urls import path
from calculator.views import show_recipe, homepage_view   

urlpatterns = [
      path('', homepage_view, name='homepage'),    # новая точка входа для /
      path('<slug:dish>/', show_recipe, name='show_recipe'),    # существующий маршрут
]