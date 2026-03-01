from django.db import models
from django.utils.text import slugify


class Phone(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Название")
    price = models.IntegerField(verbose_name="Цена")
    image = models.URLField(verbose_name="Изображение", blank=True)
    release_date = models.DateField(verbose_name="Дата выпуска", null=True, blank=True)
    lte_exists = models.BooleanField(verbose_name="LTE", default=False)
    slug = models.SlugField(max_length=255, unique=True, verbose_name="Slug")

    class Meta:
        verbose_name = "Телефон"
        verbose_name_plural = "Телефоны"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name