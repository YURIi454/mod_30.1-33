from rest_framework import serializers

from on_learning.models import Course, Lesson
from on_learning.validators import CorrectURLValidator


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для урока."""

    class Meta:
        model = Lesson
        fields = [
            "name",
            "description",
            "video",
            "course",
        ]
        validators = [CorrectURLValidator("video")]


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для курса."""

    lesson_count = serializers.SerializerMethodField()
    lesson = LessonSerializer(many=True, read_only=True, source="lesson_set")

    class Meta:
        model = Course
        fields = [
            "name",
            "description",
            "preview",
            "lesson_count",
            "lesson",
        ]

    def get_lesson_count(self, instance):
        return instance.lesson_set.count()
