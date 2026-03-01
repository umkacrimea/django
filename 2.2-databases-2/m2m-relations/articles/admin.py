from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from .models import Article, Tag, Scope


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        """Проверка: ровно один основной тег у статьи"""
        main_count = 0
        
        for form in self.forms:
            # Пропускаем пустые или помеченные на удаление формы
            if not hasattr(form, 'cleaned_data') or not form.cleaned_data:
                continue
            if form.cleaned_data.get('DELETE', False):
                continue
            if form.cleaned_data.get('is_main'):
                main_count += 1
        
        if main_count == 0:
            raise ValidationError('У статьи должен быть ровно один основной раздел')
        elif main_count > 1:
            raise ValidationError(f'У статьи может быть только один основной раздел, а отмечено {main_count}')
        
        return super().clean()


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset
    extra = 1
    verbose_name = 'Раздел статьи'
    verbose_name_plural = 'Разделы статьи'


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'published_at', 'get_tags']
    list_filter = ['scope_items__tag', 'published_at']
    search_fields = ['title', 'text']
    inlines = [ScopeInline]
    date_hierarchy = 'published_at'
    
    def get_tags(self, obj):
        return ", ".join([s.tag.name for s in obj.scope_items.all()])
    get_tags.short_description = 'Разделы'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']