from django.shortcuts import render
from .models import Student


def students_list(request):
    template = 'school/students_list.html'
    
    # Параметр сортировки (по умолчанию по классу, затем по имени)
    ordering = request.GET.get('order', 'group')
    
    # ⚡ ОПТИМИЗАЦИЯ: prefetch_related уменьшает число SQL-запросов
    # Без него: 1 запрос на ученика для получения учителей (N+1 проблема)
    # С ним: 2 запроса всего (ученики + все учителя)
    students = Student.objects.prefetch_related('teachers').order_by(ordering)
    
    context = {
        'object_list': students,  # шаблон ожидает object_list (как в ListView)
        'ordering': ordering,
    }
    return render(request, template, context)