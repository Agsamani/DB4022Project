from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('psqltest', views.psql_test, name='psql_test'),
]