from datetime import datetime


class DateConverter:
    regex = r'[0-9]{4}-[0-9]{2}-[0-9]{2}'
    format = '%Y-%m-%d'

    def to_python(self, value: str) -> datetime:
        return datetime.strptime(value, self.format).date()  # возвращаем date, не datetime!

    def to_url(self, value) -> str:
        if isinstance(value, str):
            return value
        return value.strftime(self.format)