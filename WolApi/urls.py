from django.urls import path
from . import views

urlpatterns = [
    path('user/', views.NormalUserAPIView.as_view(), name='normalUser'),
    path('login/', views.login, name='login'),
    path('test/', views.test_token, name='test'),
    path('otp-get/', views.get_otp, name='otp-get'),
]