from rest_framework import status
from rest_framework.test import APITestCase

from on_learning.models import Course, Lesson, Subscribe
from users.models import CustomUser, Payments


class TestCustomUser(APITestCase):
    """ Тест CRUD пользователя и оплаты. """

    def setUp(self):
        """ Создание тестового пользователя для авторизации. """

        self.user = CustomUser.objects.create_user(
            email='test@test.com',
            username='Auth_User_True',
            password='password123')

        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            name='Test_Course_2',
            description='Test_Course_2',
            owner=self.user,
        )

        self.lesson = Lesson.objects.create(
            name='Test_Lesson_2',
            description='Test_Lesson_2',
            owner=self.user,
            course=self.course,
        )

        self.payment = Payments.objects.create(
            name='Test_Payment_1',
            user=self.user,
            course=self.course,
            lesson=self.lesson,
        )

    def test_create_user(self):
        """ Тест создания пользователя. """

        data = {
            'email': 'user@one.com',
        }

        response = self.client.post('/users/user/create/', data=data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_update_user(self):
        """ Тест обновления пользователя. """

        data = {
            'email': 'test@test.com',
            'username': 'Auth_User_Update',
        }

        response = self.client.patch(f'/users/user/update/{self.user.id}/', data=data)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_detail_user(self):
        """ Тест вывода информации о пользователе. """

        response = self.client.get(f'/users/user/detail/{self.user.id}/')

        self.assertEqual(response.json(), {
            'email': 'test@test.com',
            'phone_number': None,
            'avatar': None}
                         )

    def test_delete_user(self):
        """ Тест удаления пользователя. """

        response = self.client.delete(f'/users/user/delete/{self.user.id}')

        self.assertEqual(
            response.status_code,
            status.HTTP_301_MOVED_PERMANENTLY
        )

    def test_create_payment(self):
        """ Тест создания платежа. """

        data = {
            'name': 'Test_Payment_2',
            'user': self.user.id,
            'course': self.course.id,
            'lesson': self.lesson.id,
            'amount': 38.4,
        }

        response = self.client.post('/users/payments/create/', data=data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_update_payment(self):
        """ Тест обновления платежа. """

        data = {
            'name': 'Test_Payment_1',
            'amount': 134.4,
        }

        response = self.client.patch(f'/users/payments/update/{self.payment.id}/', data=data)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_create_subscription(self):
        """ Тест создание подписки. """

        data = {"course_id": self.course.id}

        response = self.client.post('/subscribe/', data=data, )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Subscribe.objects.filter(user=self.user, course=self.course).exists())

    def test_remove_subscription(self):
        """ Тест удаление подписки. """

        Subscribe.objects.create(user=self.user, course=self.course)

        data = {"course_id": self.course.id}

        response = self.client.post('/subscribe/', data=data, )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Subscribe.objects.filter(user=self.user, course=self.course).exists())
