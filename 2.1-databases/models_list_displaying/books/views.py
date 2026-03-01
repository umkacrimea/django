from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Min, Max
from .models import Book


def books_view(request):
    """Страница со всеми книгами"""
    template = 'books/books_list.html'
    books = Book.objects.all().order_by('-pub_date', 'name')
    
    context = {
        'books': books,
        'page_title': 'Все книги',
        'show_pagination': False,
        'is_detail': False,
    }
    return render(request, template, context)


def books_by_date(request, pub_date):
    """Книги за конкретную дату + пагинация по датам"""
    template = 'books/books_list.html'
    
    books = Book.objects.filter(pub_date=pub_date).order_by('name')
    if not books.exists():
        from django.http import Http404
        raise Http404(f"Нет книг за дату {pub_date}")
    
    # Пагинация: поиск соседних дат
    prev_date = Book.objects.filter(pub_date__lt=pub_date).aggregate(
        max_date=Max('pub_date')
    )['max_date']
    
    next_date = Book.objects.filter(pub_date__gt=pub_date).aggregate(
        min_date=Min('pub_date')
    )['min_date']
    
    context = {
        'books': books,
        'page_title': f'Книги за {pub_date}',
        'current_date': pub_date,
        'prev_date': prev_date,
        'next_date': next_date,
        'show_pagination': True,
        'is_detail': False,
    }
    return render(request, template, context)


def book_detail(request, book_id):
    """Детальная страница одной книги"""
    template = 'books/book_detail.html'  # ← новый шаблон
    book = get_object_or_404(Book, pk=book_id)
    
    context = {
        'book': book,
    }
    return render(request, template, context)