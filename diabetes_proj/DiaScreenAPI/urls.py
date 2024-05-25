from django.urls import path
from .views import PatientCreateView, PatientListView, PatientByDoctorView, GlucoseCreateListView

urlpatterns = [
    path('create-patient', PatientCreateView.as_view(), name='create-patient'),
    path('patients', PatientListView.as_view(), name='patient_list_api'),
    path('doctor/<int:doctor_id>/patients', PatientByDoctorView.as_view(), name='doctors_patient_list'),

    # notes in patient_card

    path('patient/<str:username>/glucose-measurements', GlucoseCreateListView.as_view(), name='create_list_glucose-meas'),
]