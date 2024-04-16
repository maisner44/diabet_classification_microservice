from django.urls import path
from . import views

urlpatterns = [
    path('registration', views.registration, name='registration'),
    path('registration/patients', views.register_patient, name='patient_register'),
    path('registration/doctors', views.register_doctor, name='doctor_register'),
    path('login', views.user_login, name='login'),
]