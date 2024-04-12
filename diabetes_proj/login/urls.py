from django.urls import path
from . import views

urlpatterns = [
    path('register', views.PatientFormView.as_view(), name='register'),
]