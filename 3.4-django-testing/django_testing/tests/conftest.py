import pytest
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Course, Student


@pytest.fixture
def api_client():
    """Фикстура для API-клиента DRF"""
    return APIClient()


@pytest.fixture
def course_factory():
    """Фабрика для создания курсов через model_bakery"""
    def _factory(**kwargs):
        return baker.make(Course, **kwargs)
    return _factory


@pytest.fixture
def student_factory():
    """Фабрика для создания студентов через model_bakery"""
    def _factory(**kwargs):
        return baker.make(Student, **kwargs)
    return _factory