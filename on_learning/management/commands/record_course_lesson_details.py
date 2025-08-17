from django.core.management.base import BaseCommand
from on_learning.models import Course, Lesson


class Command(BaseCommand):
    """ Заполнение таблиц ''курс и 'урок'. """

    help = 'Заполняет базу данных курсом и уроками.'

    def handle(self, *args, **options):
        course = Course(
            name="Python-разработчик",
            description="Курс по изучению Python"
        )
        course.save()
        self.stdout.write(f'Создан курс "{course.name}"')

        lessons_list = [
            {"name": "Начало работы с Python", "description": "Установка среды разработки"},
            {"name": "Типы данных и переменные", "description": "Работа с основными типами данных"},
            {"name": "Простые функции", "description": "Условия и циклы"},
            {"name": "Библиотеки и модули", "description": "Создание функций и работа с модулями"},
            {"name": "ООП", "description": "Основы ООП"}
        ]

        lessons = []

        for data in lessons_list:
            lesson = Lesson(
                name=data["name"],
                description=data["description"],
                course=course
            )
            lessons.append(lesson)

        Lesson.objects.bulk_create(lessons)

        self.stdout.write(f"Добавлено {len(lessons_list)} уроков")
