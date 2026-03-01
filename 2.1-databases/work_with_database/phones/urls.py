from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_catalog, name='catalog'),
    path('<slug:slug>/', views.show_product, name='phone'),
]