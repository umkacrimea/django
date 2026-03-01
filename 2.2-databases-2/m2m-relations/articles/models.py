from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название', unique=True)

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'
        ordering = ['name']

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение')

    scopes = models.ManyToManyField(
        Tag,
        through='Scope',
        related_name='articles',
        verbose_name='Разделы'
    )

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-published_at']

    def __str__(self):
        return self.title


class Scope(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        verbose_name='Статья',
        related_name='scope_items'  # ← важно: не 'scopes'
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='Раздел'
    )
    is_main = models.BooleanField(default=False, verbose_name='Основной')

    class Meta:
        verbose_name = 'Связь статьи с разделом'
        verbose_name_plural = 'Связи статей с разделами'
        ordering = ['-is_main', 'tag__name']
        unique_together = ['article', 'tag']

    def __str__(self):
        return f"{self.article.title} — {self.tag.name}"