from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Phone


def index(request):
    """Редирект с корня сайта на каталог"""
    return redirect(reverse('catalog'))


def show_catalog(request):
    """Страница каталога с сортировкой"""
    # Получаем параметр сортировки из URL (?sort=...)
    sort_param = request.GET.get('sort', 'name')
    
    # Маппинг параметров на поля модели
    sort_mapping = {
        'name': 'name',           # по названию А-Я
        'min_price': 'price',     # сначала дешёвые
        'max_price': '-price',    # сначала дорогие (минус = убывание)
    }
    
    # Получаем порядок сортировки, по умолчанию — по имени
    order_by = sort_mapping.get(sort_param, 'name')
    
    # Запрос к БД с сортировкой
    phones = Phone.objects.all().order_by(order_by)
    
    context = {
        'phones': phones,
    }
    return render(request, 'catalog.html', context)


def show_product(request, slug):
    """Страница конкретного телефона"""
    # get_object_or_404 автоматически вернёт 404, если телефон не найден
    phone = get_object_or_404(Phone, slug=slug)
    
    context = {
        'phone': phone,
    }
    return render(request, 'product.html', context)