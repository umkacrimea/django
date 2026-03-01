from django.db import models


class Sensor(models.Model):
    """Программируемый датчик температуры"""
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Датчик'
        verbose_name_plural = 'Датчики'
        ordering = ['name']

    def __str__(self):
        return self.name


class Measurement(models.Model):
    """Измерение температуры датчиком"""
    sensor = models.ForeignKey(
        Sensor,
        on_delete=models.CASCADE,
        related_name='measurements',  # позволяет sensor.measurements.all()
        verbose_name='Датчик'
    )
    temperature = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        verbose_name='Температура'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время')
    
    # 🔹 Дополнительное задание: поле для изображения (опциональное)
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to='measurements/',
        verbose_name='Изображение'
    )

    class Meta:
        verbose_name = 'Измерение'
        verbose_name_plural = 'Измерения'
        ordering = ['-created_at']  # новые измерения сверху

    def __str__(self):
        return f"{self.sensor.name}: {self.temperature}°C @ {self.created_at.strftime('%H:%M')}"