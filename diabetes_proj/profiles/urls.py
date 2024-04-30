from django.urls import path
from .views import DoctorProfile, patient_profile

urlpatterns = [
    path('doctor/<int:pk>', DoctorProfile.as_view(), name='doctor_profile'),
    path('patient/<int:pk>', patient_profile, name='patient_profile'),
]