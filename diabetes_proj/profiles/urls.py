from django.urls import path
from .views import DoctorProfile, PatientProfile, DoctorsPatientList
from .views import edit_patient_profile, edit_doctor_profile, unlink_doctor

urlpatterns = [
    path('doctor/<int:pk>', DoctorProfile.as_view(), name='doctor_profile'),
    path('patient/<int:pk>', PatientProfile.as_view(), name='patient_profile'),
    path('doctor/patients', DoctorsPatientList.as_view(), name='patient_list'),
    path('edit_patient/<int:patient_id>', edit_patient_profile, name='edit_patient'),
    path('edit_doctor/<int:doctor_id>', edit_doctor_profile, name='edit_doctor'),
    path('patient/unlink-doctor', unlink_doctor, name='unlink_doctor'),
]