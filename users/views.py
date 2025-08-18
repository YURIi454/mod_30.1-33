from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import permissions

from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView

from users.models import Payments, CustomUser
from users.serializers import PaymentsSerializer, CustomUserSerializer


class CustomUserDetail(RetrieveAPIView):
    """ Просмотр данных пользователя. """

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class PaymentCreateAPIView(CreateAPIView):
    """ Создание платежа. """

    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    permission_classes = [permissions.AllowAny]


class PaymentListAPIView(ListAPIView):
    """ Список платежей. """

    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    search_fields = ["course", "lesson", "payment_method"]
    ordering_fields = ["payment_day"]
    ordering = ["-payment_day"]
