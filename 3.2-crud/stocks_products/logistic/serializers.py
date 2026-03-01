from rest_framework import serializers
from logistic.models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для продукта"""
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']
        # search_fields будет задан во views


class ProductPositionSerializer(serializers.ModelSerializer):
    """Сериализатор для позиции товара на складе"""
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    """Сериализатор для склада с вложенными позициями"""
    positions = ProductPositionSerializer(many=True, write_only=True, required=False)
    
    # Для чтения: показываем позиции с деталями продукта
    positions_read = ProductPositionSerializer(
        source='positions', 
        many=True, 
        read_only=True
    )

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions', 'positions_read']
        # positions — для записи, positions_read — для чтения

    def create(self, validated_data):
        """Создание склада с позициями"""
        positions_data = validated_data.pop('positions', [])
        
        # Создаём склад
        stock = Stock.objects.create(**validated_data)
        
        # Создаём позиции
        for position_data in positions_data:
            StockProduct.objects.create(stock=stock, **position_data)
        
        return stock

    def update(self, instance, validated_data):
        """Обновление склада с позициями"""
        positions_data = validated_data.pop('positions', None)
        
        # Обновляем поля склада
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Обновляем позиции (если переданы)
        if positions_data is not None:
            # Удаляем старые позиции
            instance.positions.all().delete()
            
            # Создаём новые
            for position_data in positions_data:
                StockProduct.objects.create(stock=instance, **position_data)
        
        return instance