from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from users.models import CustomUser


class Command(BaseCommand):
    """ Создание тестового пользователя. """

    help = "Создание тестового пользователя."

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, default='test@example.com', help='E-mail.')
        parser.add_argument('--password', type=str, default='testpass', help='Пароль.')

    def handle(self, *args, **options):
        email = options['email']
        password = options['password']

        if CustomUser.objects.filter(email=email).exists():
            self.stdout.write(f"Пользователь с таким '{email}' уже существует!")
            return

        test_user = CustomUser(
            email=email,
            username=f'test_{email.split("@")[0]}',
            is_active=True,
            is_staff=False,
            is_superuser=False,
        )
        test_user.set_password(password)
        test_user.save()

        self.stdout.write(f"Тестовый пользователь с e-mail '{email}' успешно создан!")
