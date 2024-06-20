from django.urls import path
from . import views

urlpatterns = [
    path('user/', views.UserAPIView.as_view(), name='normalUser'),
    path('admin/', views.AdminAPIView.as_view(), name='admin'),
    path('login/', views.login, name='login'),
    path('admin-login/', views.admin_login, name='login'),
    path('get-otp/', views.get_otp, name='otp-get'),
    path('admin-get-otp/', views.admin_get_otp, name='otp-get'),
    path('adv/', views.AdvertisementAPIView.as_view(), name='otp-get'),
    path('test/', views.test_token, name='test'),
]