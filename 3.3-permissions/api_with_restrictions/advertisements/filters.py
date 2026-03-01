from django_filters import rest_framework as filters
from django_filters.filters import DateFromToRangeFilter
from advertisements.models import Advertisement
from advertisements.models import Advertisement, AdvertisementStatusChoices

class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""
    
    # 🔍 Фильтр по дате создания (диапазон)
    created_at = DateFromToRangeFilter(field_name='created_at')
    
    # 🔍 Фильтр по статусу (точное совпадение)
    status = filters.ChoiceFilter(
        choices=AdvertisementStatusChoices.choices,
        lookup_expr='exact'
    )

    class Meta:
        model = Advertisement
        # 🔹 fields автоматически создаст фильтры для указанных полей
        fields = ['id', 'status', 'creator', 'created_at']