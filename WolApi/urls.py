from django.urls import path
from . import views

urlpatterns = [
    path('user/', views.UserAPIView.as_view(), name='normalUser'),
    path('user/update', views.update_user_profile, name='updateUserProfile'),
    path('user/adv', views.get_user_ads, name='getUserAds'),
    path('user/new-business', views.new_business, name='newBusiness'),

    path('user/<int:pub_id>/deactivate', views.deactivate_user, name='newBusiness'),

    path('admin/', views.AdminAPIView.as_view(), name='admin'),
    path('login/', views.login, name='login'),
    path('admin-login/', views.admin_login, name='login'),
    path('get-otp/', views.get_otp, name='otpGet'),
    path('admin-get-otp/', views.admin_get_otp, name='adminOtpGet'),
    path('adv/', views.AdvertisementAPIView.as_view(), name='adView'),
    path('logout/', views.logout, name='logout'),

    path('test/', views.test_token, name='test'),
    path('file-test/', views.file_test, name='fileTest'),

    path('admin/ad-check/<int:ad_id>', views.admin_update_ad_status, name='adminUpdateAdStatus'),

    path('adv/latest/', views.get_latest_ads, name='latestAds'),
    path('adv/<int:ad_id>/', views.get_ad_detail, name='adDetail'),
    path('adv/<int:ad_id>/report', views.report_ad, name='reportAd'),
    path('adv/<int:ad_id>/get-reports', views.get_ad_reports, name='getReportAd'),
    path('adv/<int:ad_id>/deactivate', views.deactivate_ad, name='deactivateAd'),

    path('adv/search', views.search_advertisement, name='searchAd'),
]