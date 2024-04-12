from django.urls import path
from . import views

urlpatterns = [
    path('registration', views.register_patient, name='registration'),
    path('login', views.user_login, name='login'),
]