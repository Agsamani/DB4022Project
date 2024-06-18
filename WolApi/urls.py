from django.urls import path
from . import views

urlpatterns = [
    path('user/', views.NormalUserAPIView.as_view(), name='normalUser'),
]