# coding=utf-8
from django.db import models


class Book(models.Model):
    name = models.CharField('Название', max_length=64)
    author = models.CharField('Автор', max_length=64)
    pub_date = models.DateField('Дата публикации')

    class Meta:
        ordering = ['-pub_date', 'name']  # сортировка по умолчанию
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        return f"{self.name} — {self.author}"