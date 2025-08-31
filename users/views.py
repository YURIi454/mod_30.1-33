from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated

from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView, RetrieveUpdateAPIView)

from users.models import Payments, CustomUser
from users.permissions import OwnerOnlyPerm
from users.serializers import PaymentsSerializer, CustomUserSerializer


# region CRUD user
class CreateCustomUser(CreateAPIView):
    """ Создание пользователя. """

    serializer_class = CustomUserSerializer


class UpdateCustomUser(RetrieveUpdateAPIView):
    """ Редактирование пользователя. """

    filter_backends = [DjangoFilterBackend, OrderingFilter,]
    permission_classes = [IsAuthenticated, ]
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        return CustomUser.objects.filter(id=self.request.user.id)


class CustomUserDetail(RetrieveAPIView):
    """ Просмотр данных пользователя. """

    filter_backends = [DjangoFilterBackend, OrderingFilter,]
    permission_classes = [IsAuthenticated, ]
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        return CustomUser.objects.filter(id=self.request.user.id)


class DeleteCustomUser(DestroyAPIView):
    """ Удаление пользователя. """

    permission_classes = [IsAuthenticated, OwnerOnlyPerm, ]

    def get_queryset(self):
        return CustomUser.objects.filter(id=self.request.user.id)


# endregion

# region CRUD payment
class PaymentCreateAPIView(CreateAPIView):
    """ Создание платежа. """

    permission_classes = [IsAuthenticated, ]
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer


class PaymentListAPIView(ListAPIView):
    """ Список платежей. """

    permission_classes = [IsAuthenticated, OwnerOnlyPerm, ]
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter,]
    search_fields = ["course", "lesson", "payment_method"]
    ordering_fields = ["payment_day"]
    ordering = ["-payment_day"]


class PaymentUpdateAPIView(UpdateAPIView):
    """ Обновление платежа. """

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    permission_classes = [IsAuthenticated,]
    serializer_class = PaymentsSerializer

    def get_queryset(self):
        return Payments.objects.filter(user=self.request.user)


class PaymentDeleteAPIView(DestroyAPIView):
    """ Удаление платежа. """

    permission_classes = [IsAuthenticated, OwnerOnlyPerm, ]
    queryset = Payments.objects.all()

# endregion
