from django.db import models
from django.db.models import RESTRICT


class Course(models.Model):
    """ Курс """

    name = models.CharField(unique=True, max_length=150)
    description = models.TextField(max_length=1000)
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
