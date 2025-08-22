from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from on_learning.models import Course, Lesson
from on_learning.serializers import CourseSerializer, LessonSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from users.permissions import OwnerOrManagerPerm, OwnerOnlyPerm


# region CRUD для курса

class CourseCreateAPIView(CreateAPIView):
    """ Создание курса. """

    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """ Заполнение поля owner данными текущего пользователя. """

        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()


class CourseViewSet(ModelViewSet):
    """ Представление для курса. """

    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsAuthenticated]


class CourseUpdateAPIView(UpdateAPIView):
    """ Обновление курса. """

    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [OwnerOrManagerPerm]


class CourseDeleteAPIView(DestroyAPIView):
    """ Удаление курса. """

    serializer_class = CourseSerializer
    permission_classes = [OwnerOnlyPerm]

# endregion

# region CRUD для урока
class LessonCreateAPIView(CreateAPIView):
    """ Создание урока. """

    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """ Заполнение поля owner данными текущего пользователя. """

        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(ListAPIView):
    """ Просмотр списка уроков. """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    search_fields = ["name", "description", "course"]
    ordering_fields = ["name"]
    ordering = ["-name"]
    permission_classes = [IsAuthenticated]


class LessonRetrieveAPIView(RetrieveAPIView):
    """ Просмотр одного урока. """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]


class LessonUpdateAPIView(UpdateAPIView):
    """ Обновление одного урока. """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [OwnerOrManagerPerm]


class LessonDeleteAPIView(DestroyAPIView):
    """ Удаление урока. """

    queryset = Lesson.objects.all()
    permission_classes = [OwnerOnlyPerm]
# endregion
