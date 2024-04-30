from django.urls import path
from .views import DoctorProfile, PatientProfile

urlpatterns = [
    path('doctor/<int:pk>', DoctorProfile.as_view(), name='doctor_profile'),
    path('patient/<int:pk>', PatientProfile.as_view(), name='patient_profile'),
]