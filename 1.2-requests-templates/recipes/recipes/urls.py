from django.urls import path
from calculator.views import show_recipe   

urlpatterns = [
      path('', show_recipe, name='show_recipe'),                   # Главное меню (выбор рецепта)
      path('<slug:dish>/', show_recipe, name='show_recipe'),       # Отдельный рецепт
]