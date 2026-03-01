from django.conf import settings
from rest_framework import serializers
from students.models import Course


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "students")
    
    def validate(self, data):
        """Проверка лимита студентов на курсе"""
        students = data.get('students')
        if students is not None:
            max_students = getattr(settings, 'MAX_STUDENTS_PER_COURSE', 20)
            if len(students) > max_students:
                raise serializers.ValidationError(
                    {'students': f"Cannot add more than {max_students} students to a course"}
                )
        return data