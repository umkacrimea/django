from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from logistic.models import Product, Stock
from logistic.serializers import ProductSerializer, StockSerializer


class ProductViewSet(ModelViewSet):
    """CRUD для продуктов + поиск по названию/описанию"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    # 🔍 Подключаем бэкенды фильтрации и поиска
    filter_backends = [DjangoFilterBackend, SearchFilter]
    
    # Фильтрация по точному совпадению
    filterset_fields = ['id', 'title']
    
    # 🔍 Поиск по частичному совпадению (case-insensitive)
    search_fields = ['title', 'description']


class StockViewSet(ModelViewSet):
    """CRUD для складов + поиск по продуктам"""
    queryset = Stock.objects.prefetch_related('positions__product').all()
    serializer_class = StockSerializer
    
    # 🔍 Подключаем фильтрацию
    filter_backends = [DjangoFilterBackend]
    
    # 🔍 Фильтрация по продуктам:
    # - ?product=123 — по ID продукта
    # - ?search=помид — по названию/описанию продукта (доп. задание)
    filterset_fields = ['products__id', 'products__title']
    
    # 🔍 Поиск по продуктам внутри склада (доп. задание)
    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search')
        
        if search:
            # Ищем склады, где есть продукты с таким названием или описанием
            queryset = queryset.filter(
                products__title__icontains=search
            ).distinct() | queryset.filter(
                products__description__icontains=search
            ).distinct()
        
        return queryset