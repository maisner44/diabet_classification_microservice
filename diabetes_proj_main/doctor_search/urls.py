from django.urls import path
from .views import DoctorSearchView

urlpatterns = [
    path('', DoctorSearchView.as_view(template_name = 'doctor_list.html'), name='doctors_search'),
]