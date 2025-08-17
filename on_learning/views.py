from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from on_learning.models import Course, Lesson
from on_learning.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(ModelViewSet):
    """ Представление для курса. """

    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]


class LessonCreateAPIView(CreateAPIView):
    """ Создание урока. """

    serializer_class = LessonSerializer
    permission_classes = [permissions.AllowAny]


class LessonListAPIView(ListAPIView):
    """ Просмотр списка уроков. """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    search_fields = ["name", "description", "course"]
    ordering_fields = ["name"]
    ordering = ["-name"]


class LessonRetrieveAPIView(RetrieveAPIView):
    """ Просмотр одного урока. """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(UpdateAPIView):
    """ Обновление одного урока. """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [permissions.AllowAny]


class LessonDeleteAPIView(DestroyAPIView):
    """ Удаление урока. """

    queryset = Lesson.objects.all()
    permission_classes = [permissions.AllowAny]
