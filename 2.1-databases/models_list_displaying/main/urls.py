from django.contrib import admin
from django.urls import path, register_converter
from django.shortcuts import redirect
from books.views import books_view, books_by_date, book_detail
from books.converters import DateConverter

register_converter(DateConverter, 'date')


def root_redirect(request):
    return redirect('books')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', root_redirect, name='root'),
    
    path('books/', books_view, name='books'),
    path('books/<date:pub_date>/', books_by_date, name='books_by_date'),
    path('books/book/<int:book_id>/', book_detail, name='book_detail'),  # ← новая страница
]