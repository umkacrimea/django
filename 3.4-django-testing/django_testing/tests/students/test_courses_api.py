import pytest
from model_bakery import baker

from students.models import Course, Student


@pytest.mark.django_db
def test_retrieve_course(api_client, course_factory):
    """Проверка получения одного курса (retrieve)"""
    # Создаём курс через фабрику
    course = course_factory(name="Test Course")
    
    # Делаем запрос
    url = f"/api/v1/courses/{course.id}/"
    response = api_client.get(url)
    
    # Проверяем результат
    assert response.status_code == 200
    assert response.data["id"] == course.id
    assert response.data["name"] == course.name


@pytest.mark.django_db
def test_list_courses(api_client, course_factory):
    """Проверка получения списка курсов (list)"""
    # Создаём несколько курсов
    courses = course_factory(_quantity=3)
    
    # Делаем запрос к списку
    url = "/api/v1/courses/"
    response = api_client.get(url)
    
    # Проверяем результат
    assert response.status_code == 200
    assert len(response.data) == 3
    returned_ids = [c["id"] for c in response.data]
    for course in courses:
        assert course.id in returned_ids


@pytest.mark.django_db
def test_filter_courses_by_id(api_client, course_factory):
    """Проверка фильтрации курсов по id"""
    # Создаём курсы
    course1 = course_factory(name="Course 1")
    course2 = course_factory(name="Course 2")
    
    # Фильтруем по ID первого курса
    url = f"/api/v1/courses/?id={course1.id}"
    response = api_client.get(url)
    
    # Проверяем результат
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["id"] == course1.id


@pytest.mark.django_db
def test_filter_courses_by_name(api_client, course_factory):
    """Проверка фильтрации курсов по name"""
    # Создаём курсы
    course_factory(name="Python Course")
    course_factory(name="Java Course")
    
    # Фильтруем по имени
    url = "/api/v1/courses/?name=Python Course"
    response = api_client.get(url)
    
    # Проверяем результат
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["name"] == "Python Course"


@pytest.mark.django_db
def test_create_course(api_client):
    """Тест успешного создания курса"""
    # Готовим данные
    data = {
        "name": "New Course",
        "students": []
    }
    
    # Делаем POST-запрос
    url = "/api/v1/courses/"
    response = api_client.post(url, data, format="json")
    
    # Проверяем результат
    assert response.status_code == 201
    assert response.data["name"] == "New Course"
    assert Course.objects.filter(id=response.data["id"]).exists()


@pytest.mark.django_db
def test_update_course(api_client, course_factory):
    """Тест успешного обновления курса"""
    # Создаём курс
    course = course_factory(name="Old Name")
    
    # Данные для обновления
    data = {
        "name": "Updated Name",
        "students": []
    }
    
    # Делаем PUT-запрос
    url = f"/api/v1/courses/{course.id}/"
    response = api_client.put(url, data, format="json")
    
    # Проверяем результат
    assert response.status_code == 200
    assert response.data["name"] == "Updated Name"
    
    # Дополнительно проверяем в БД
    course.refresh_from_db()
    assert course.name == "Updated Name"


@pytest.mark.django_db
def test_delete_course(api_client, course_factory):
    """Тест успешного удаления курса"""
    # Создаём курс
    course = course_factory()
    
    # Делаем DELETE-запрос
    url = f"/api/v1/courses/{course.id}/"
    response = api_client.delete(url)
    
    # Проверяем статус
    assert response.status_code == 204
    
    # Проверяем, что курс удалён из БД
    assert not Course.objects.filter(id=course.id).exists()

@pytest.mark.django_db
def test_course_student_limit_success(api_client, course_factory, student_factory, settings):
    """Тест: добавление допустимого количества студентов"""
    # Переопределяем настройку для теста
    settings.MAX_STUDENTS_PER_COURSE = 3
    
    course = course_factory()
    students = student_factory(_quantity=3)
    
    data = {
        "name": course.name,
        "students": [s.id for s in students]
    }
    
    url = f"/api/v1/courses/{course.id}/"
    response = api_client.put(url, data, format="json")
    
    assert response.status_code == 200


@pytest.mark.django_db
def test_course_student_limit_failure(api_client, course_factory, student_factory, settings):
    """Тест: попытка добавить больше студентов, чем разрешено"""
    # Переопределяем настройку для теста
    settings.MAX_STUDENTS_PER_COURSE = 3
    
    course = course_factory()
    students = student_factory(_quantity=4)  # Превышаем лимит
    
    data = {
        "name": course.name,
        "students": [s.id for s in students]
    }
    
    url = f"/api/v1/courses/{course.id}/"
    response = api_client.put(url, data, format="json")
    
    assert response.status_code == 400
    assert "students" in response.data