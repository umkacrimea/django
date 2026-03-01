import csv
import os
from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand
from phones.models import Phone
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Импортирует телефоны из CSV-файла'

    def handle(self, *args, **options):
        # Берём путь из настроек или используем относительный
        csv_path = getattr(settings, 'PHONES_CSV', 'phones.csv')
        
        if not os.path.exists(csv_path):
            # Пробуем найти файл относительно корня проекта
            csv_path = os.path.join(settings.BASE_DIR, 'phones.csv')
        
        if not os.path.exists(csv_path):
            self.stderr.write(self.style.ERROR(f'❌ Файл не найден: {csv_path}'))
            return

        with open(csv_path, 'r', encoding='utf-8') as file:
            # ⚠️ delimiter=';' — потому что в файле точки с запятой
            phones = list(csv.DictReader(file, delimiter=';'))

        created = 0
        updated = 0
        
        for phone_data in phones:
            # Очистка полей от пробелов (в CSV есть лишние пробелы в URL)
            name = phone_data['name'].strip()
            image = phone_data['image'].strip()
            price = int(phone_data['price'].strip())
            
            # Парсинг даты
            release_date_str = phone_data['release_date'].strip()
            release_date = None
            if release_date_str:
                try:
                    release_date = datetime.strptime(release_date_str, '%Y-%m-%d').date()
                except ValueError:
                    release_date = None
            
            # Конвертация булевого значения
            lte_raw = phone_data['lte_exists'].strip().lower()
            lte_exists = lte_raw in ('true', '1', 'yes', 'да')
            
            # Генерация slug
            slug = slugify(name)
            
            # Создаём или обновляем запись
            obj, is_created = Phone.objects.update_or_create(
                slug=slug,
                defaults={
                    'name': name,
                    'price': price,
                    'image': image,
                    'release_date': release_date,
                    'lte_exists': lte_exists,
                }
            )
            
            if is_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'✅ Импорт завершён: создано {created}, обновлено {updated} записей'
            )
        )