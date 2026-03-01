from django.db import models


class Teacher(models.Model):
    name = models.CharField(max_length=30, verbose_name='Имя')
    subject = models.CharField(max_length=20, verbose_name='Предмет')  # увеличил max_length

    class Meta:
        verbose_name = 'Учитель'
        verbose_name_plural = 'Учителя'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.subject})"


class Student(models.Model):
    name = models.CharField(max_length=30, verbose_name='Имя')
    # ← МЕНЯЕМ: ForeignKey → ManyToManyField
    teachers = models.ManyToManyField(
        Teacher,
        verbose_name='Учителя',
        related_name='students'  # позволяет teacher.students.all()
    )
    group = models.CharField(max_length=10, verbose_name='Класс')

    class Meta:
        verbose_name = 'Ученик'
        verbose_name_plural = 'Ученики'
        ordering = ['group', 'name']

    def __str__(self):
        return f"{self.name} ({self.group})"