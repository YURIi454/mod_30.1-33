from django.db import models
from django.db.models import CASCADE, RESTRICT, SET_NULL

from config.settings import AUTH_USER_MODEL


class Course(models.Model):
    """ Курс """

    name = models.CharField(unique=True, max_length=150)
    description = models.TextField(max_length=1000)
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=SET_NULL, blank=True, null=True, verbose_name='владелец')
    preview = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name='Изображение')
    created_at = models.DateTimeField(auto_now=True, verbose_name='Добавлен')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='Изменён')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['name']


class Lesson(models.Model):
    """ Урок """

    name = models.CharField(unique=True, max_length=150)
    description = models.TextField(max_length=1000)
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=SET_NULL, blank=True, null=True, verbose_name='владелец')
    preview = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name='Изображение')
    video = models.URLField(null=True, blank=True, verbose_name='Ссылка на видео')
    course = models.ForeignKey(Course, on_delete=RESTRICT, verbose_name='Курс')
    created_at = models.DateTimeField(auto_now=True, verbose_name='Добавлен')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='Изменён')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['name']


class Subscribe(models.Model):
    """ Подписка. """

    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=CASCADE, verbose_name='Пользователь')
    course = models.ForeignKey(Course, on_delete=CASCADE, verbose_name='Курс')
    status_sub = models.BooleanField(default=True, verbose_name='Статус подписки')
    description = models.TextField(max_length=150, blank=True, null=True, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now=True, verbose_name='Добавлена')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='Изменена')

    def __str__(self):
        return f'{self.user} {self.course}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = ['user', 'course']
        ordering = ['user']
