from django.urls import path
from rest_framework.routers import DefaultRouter

from on_learning.views import (
    CourseViewSet,
    LessonCreateAPIView,
    LessonDeleteAPIView,
    LessonListAPIView,
    LessonRetrieveAPIView,
    LessonUpdateAPIView,
    ProductPriceCreateAPIView,
    SubscribeView)

app_name = 'on_learning'

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
                  path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
                  path('lesson/list/', LessonListAPIView.as_view(), name='lesson_list'),
                  path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_detail'),
                  path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson_update'),
                  path('lesson/delete/<int:pk>/', LessonDeleteAPIView.as_view(), name='lesson_delete'),
                  path('subscribe/', SubscribeView.as_view(), name='subscribe'),
                  path('product_create/', ProductPriceCreateAPIView.as_view(), name='product_create'), ] + router.urls
