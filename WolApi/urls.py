from django.urls import path
from . import views

urlpatterns = [
    path('', views.sandbox, name='sandbox'),
    path('add/', views.sandbox_add, name='add'),
]