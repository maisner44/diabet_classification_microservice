from django.urls import path
from .views import DoctorProfile, PatientProfile, DoctorsPatientList

urlpatterns = [
    path('doctor/<int:pk>', DoctorProfile.as_view(), name='doctor_profile'),
    path('patient/<int:pk>', PatientProfile.as_view(), name='patient_profile'),
    path('doctor/patients', DoctorsPatientList.as_view(), name='patient_list'),
]