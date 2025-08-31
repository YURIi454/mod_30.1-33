from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import DO_NOTHING, CASCADE


class CustomUser(AbstractUser):
    """ Пользователь. """

    email = models.EmailField(unique=True, verbose_name="Ваш Email")
    phone_number = models.CharField(null=True, blank=True, verbose_name='Телефон')
    avatar = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name='Аватар')
    created_at = models.DateTimeField(auto_now=True, verbose_name='Добавлен')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='Изменён')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", ]

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['email']


class Payments(models.Model):
    """ Платежи. """

    pay_met_list = [
        ('cache', 'наличные'),
        ('transfer', 'перевод'),
        ('bonuses', 'бонусы и акции')
    ]

    name = models.CharField(unique=True, max_length=150, verbose_name='номер платежа')
    user = models.ForeignKey(CustomUser, on_delete=CASCADE, verbose_name='оплатил', )
    course = models.ForeignKey('on_learning.Course', on_delete=DO_NOTHING, verbose_name='курс', )
    lesson = models.ForeignKey('on_learning.Lesson', on_delete=DO_NOTHING, verbose_name='урок', )
    payment_day = models.DateTimeField(null=True, blank=True, verbose_name='дата платежа')
    amount = models.DecimalField(default=0.0, decimal_places=2, max_digits=8, verbose_name='сумма')
    payment_method = models.CharField(choices=pay_met_list, default='transfer',
                                      verbose_name='способ оплаты')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='изменён')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Платёж'
        verbose_name_plural = 'Платежи'
        ordering = ['payment_day']
