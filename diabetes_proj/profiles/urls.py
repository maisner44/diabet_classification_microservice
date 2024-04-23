from django.urls import path
from .views import DoctorProfile

urlpatterns = [
    path('doctor/<int:pk>', DoctorProfile.as_view(), name='doctor_profile'),
]