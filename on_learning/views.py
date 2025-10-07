from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from on_learning.models import Course, Lesson, Subscribe

# from on_learning.paginators import LessonPagination TODO заданы глобальные настройки пагинации
from on_learning.serializers import CourseSerializer, LessonSerializer
from on_learning.tasks import send_mail_course_update
from users.models import CustomUser
from users.permissions import OwnerOnlyPerm, OwnerOrManagerPerm
from users.serializers import PaymentsSerializer
from users.services import create_stripe_price_amount, create_stripe_session


# region CRUD для курса


class CourseCreateAPIView(CreateAPIView):
    """Создание курса."""

    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Заполнение поля owner данными текущего пользователя."""

        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()


class CourseViewSet(ModelViewSet):
    """Представление для курса."""

    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsAuthenticated]


class CourseUpdateAPIView(UpdateAPIView):
    """Обновление курса."""

    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [OwnerOrManagerPerm]

    def perform_update(self, serializer):
        course = serializer.save()
        send_mail_course_update.delay(course.pk)


class CourseDeleteAPIView(DestroyAPIView):
    """Удаление курса."""

    serializer_class = CourseSerializer
    permission_classes = [OwnerOnlyPerm]


# endregion


# region CRUD для урока
class LessonCreateAPIView(CreateAPIView):
    """Создание урока."""

    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Заполнение поля owner данными текущего пользователя."""

        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(ListAPIView):
    """Просмотр списка уроков."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    search_fields = ["name", "description", "course"]
    ordering_fields = ["name"]
    ordering = ["-name"]
    permission_classes = [IsAuthenticated]


class LessonRetrieveAPIView(RetrieveAPIView):
    """Просмотр одного урока."""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]


class LessonUpdateAPIView(UpdateAPIView):
    """Обновление одного урока."""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [OwnerOrManagerPerm]


class LessonDeleteAPIView(DestroyAPIView):
    """Удаление урока."""

    queryset = Lesson.objects.all()
    permission_classes = [OwnerOnlyPerm]


# endregion


# region подписка
class SubscribeView(APIView):
    """Добавление и удаление подписки пользователя."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        course_id = request.data.get("course_id")
        course = get_object_or_404(Course, id=course_id)

        subscribe = Subscribe.objects.filter(user=user, course=course)

        if subscribe.exists():
            subscribe.delete()
            return Response(status=204)
        else:
            Subscribe.objects.create(user=user, course=course)
            return Response(status=201)


# endregion


class ProductPriceCreateAPIView(CreateAPIView):
    """Создание цены продукта."""

    serializer_class = PaymentsSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        pay = serializer.save(user=self.request.user)
        price = create_stripe_price_amount(pay.product_name, pay.amount)
        session_id, session_link = create_stripe_session(price)
        pay.session_id = session_id
        pay.link = session_link
        pay.save()
