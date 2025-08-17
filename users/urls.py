from django.urls import path

from users.views import CustomUserDetail, PaymentListAPIView

app_name = 'users'

urlpatterns = [
    path('user/detail/<int:pk>/', CustomUserDetail.as_view(), name='user_detail'),
    path('payments/list/', PaymentListAPIView.as_view(), name='payment_list'),
]
