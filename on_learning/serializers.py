from rest_framework import serializers
from on_learning.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    """ Сериализатор для курса."""

    class Meta:
        model = Course
        fields = ['name', 'description', 'preview', ]


class LessonSerializer(serializers.ModelSerializer):
    """ Сериализатор для урока."""

    class Meta:
        model = Lesson
        fields = ['name', 'description', 'video', 'course', ]
