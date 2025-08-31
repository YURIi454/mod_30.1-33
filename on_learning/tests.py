from rest_framework.test import APITestCase
from rest_framework import status

from on_learning.models import Course, Lesson
from users.models import CustomUser


class TestCourseLesson(APITestCase):
    """ Тест курса и урока. """

    def setUp(self) -> None:
        """ Создание тестового пользователя для авторизации. """

        self.user = CustomUser.objects.create_user(
            email='test@test.com',
            username='TesTUser',
            password='password123')

        self.course = Course.objects.create(
            name='Test_Course_1',
            description='Test_Course_1',
            owner=self.user)

        self.lesson = Lesson.objects.create(
            name='Test_Lesson_3',
            description='Test_Lesson_3',
            owner=self.user,
            course=self.course,
        )

        self.client.force_authenticate(user=self.user)

    def test_create_course(self):
        """ Тест создание курса. """

        data = {
            'name': 'Test_course_2',
            'description': 'Test_course_2',
            'owner': self.user.id,
        }

        response = self.client.post('/course/', data=data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(response.json(),
                         {'name': 'Test_course_2',
                          'description': 'Test_course_2',
                          'preview': None,
                          'lesson_count': 0,
                          'lesson': []})

        self.assertTrue(
            Course.objects.all().exists()
        )

    def test_create_lesson(self):
        """ Тест создание урока. """

        data = {
            'name': 'Test_lesson',
            'description': 'Test_lesson',
            'owner': self.user.id,
            'course': self.course.id,
        }

        response = self.client.post('/lesson/create/', data=data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertTrue(self.course.lesson_set.filter(name='Test_lesson').exists())

        self.assertEqual(response.json(),
                         {'name': 'Test_lesson',
                          'description': 'Test_lesson',
                          'video': None, 'course': 3})

    def test_update_lesson(self):
        """ Тест обновление урока. """

        data = {
            'name': 'Test_lesson_update',
            'description': 'Test_lesson_update',
            'owner': self.user.id,
            'course': self.course.id,
        }

        self.client.patch(f'/lesson/update/{self.lesson.id}', data=data)

        self.assertTrue(
            Lesson.objects.all().count(),0
        )

    def test_delete_lesson(self):
        """ Тест удаления урока. """

        response = self.client.delete(f'/lesson/delete/{self.lesson.id}')

        self.assertEqual(
            response.status_code,
            status.HTTP_301_MOVED_PERMANENTLY
        )
