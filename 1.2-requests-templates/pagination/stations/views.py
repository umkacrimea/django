import csv
from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    # 1. Читаем данные из CSV-файла
    csv_path = settings.BUS_STATION_CSV
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        stations = list(reader)  # Преобразуем в список для пагинации

    # 2. Создаём пагинатор: 20 записей на страницу
    paginator = Paginator(stations, 20)
    
    # 3. Получаем номер страницы из GET-параметра
    page_number = request.GET.get('page')
    
    # 4. Получаем объект страницы (get_page безопасен: вернёт последнюю при неверном номере)
    page_obj = paginator.get_page(page_number)

    # 5. Формируем контекст
    context = {
        'bus_stations': page_obj,  # Page object итерируемый, подойдёт для {% for %}
        'page': page_obj,          # Для навигации в шаблоне
    }
    return render(request, 'stations/index.html', context)