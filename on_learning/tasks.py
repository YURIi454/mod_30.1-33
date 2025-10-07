from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from config.settings import EMAIL_HOST
from on_learning.models import Course, Subscribe
from users.models import CustomUser


@shared_task
def send_mail_course_update(course_id):
    """ Рассылка уведомлений об обновлении. """

    course: Course = Course.objects.get(id=course_id)
    subscribers = Subscribe.objects.filter(course=course).select_related('user')

    recipients = []

    for sub in subscribers:
        if sub.user.email:
            recipients.append(sub.user.email)

    if not recipients:
        return

    send_mail(
        subject=f"Курс '{course.name}' обновлён!",
        message=f"Мы обновили курс '{course.name}' ! Ждём Вас на нашей платформе!",
        from_email=EMAIL_HOST,
        recipient_list=recipients,
        fail_silently=False,
    )


@shared_task
def check_active_status_user():
    """ Проверка активности пользователя. """

    time_zone = timezone.now() - timedelta(days=30)
    users_to_deactivate = CustomUser.objects.filter(last_login__lt=time_zone, is_active=True)
    users_to_deactivate.update(is_active=False)
