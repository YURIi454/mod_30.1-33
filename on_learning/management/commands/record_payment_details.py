from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils.timezone import now

from on_learning.models import Course, Lesson
from users.models import CustomUser, Payments


class Command(BaseCommand):
    """ Заполнение таблицы 'платежи'. """

    help = "Заполнение таблицы 'платежи'. "

    def handle(self, *args, **kwargs):

        user = CustomUser.objects.first()
        course = Course.objects.first()
        lesson = Lesson.objects.first()
        pay_day = now()

        if not user:
            self.stdout.write("Пользователь не найден!")
            return

        if not course or not lesson:
            self.stdout.write("Данные по курсу или уроку не найдены!")
            return

        payments_list = [
            {
                "name": "PU-34513",
                "user": user,
                "course": course,
                "lesson": lesson,
                "payment_day": pay_day,
                "amount": Decimal("15000.00"),
                "payment_method": "transfer",
            },
            {
                "name": "PU-34514",
                "user": user,
                "course": course,
                "lesson": lesson,
                "payment_day": pay_day,
                "amount": Decimal("25000.00"),
                "payment_method": "cache",
            },
            {
                "name": "PU-34515",
                "user": user,
                "course": course,
                "lesson": lesson,
                "payment_day": pay_day,
                "amount": Decimal("30000.00"),
                "payment_method": "bonuses",
            },
        ]

        try:
            new_payments = [Payments(**data) for data in payments_list]
            Payments.objects.bulk_create(new_payments)
            self.stdout.write("Таблица успешно заполнена данными о платежах.")

        except Exception as e:
            self.stderr.write(f"Ошибка при заполнена данными: {e}")
