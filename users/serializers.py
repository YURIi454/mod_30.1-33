from rest_framework import serializers
from users.models import CustomUser, Payments


class CustomUserSerializer(serializers.ModelSerializer):
    """ Сериализатор для пользователя."""

    class Meta:
        model = CustomUser
        fields = ['email', 'phone_number', 'avatar', ]


class PaymentsSerializer(serializers.ModelSerializer):
    """ Сериализатор для оплаты."""

    class Meta:
        model = Payments
        fields = ['name', 'user', 'course', 'lesson', 'payment_day', 'amount', 'payment_method', ]
