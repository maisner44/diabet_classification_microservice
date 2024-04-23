from typing import Any
from django.shortcuts import render
from django.views import generic
from login.models import Doctor

# Create your views here.
class DoctorProfile(generic.DetailView):
    model = Doctor
    template_name = 'doctor_profile.html'
    context_object_name = 'doctor'

    @staticmethod
    def users_role(request):
        user = request.user
        is_patient = user.groups.filter(name='Patients').exists()
        is_doctor = user.groups.filter(name='Doctors').exists()
        return is_patient, is_doctor

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        is_patient, is_doctor = self.users_role(self.request)
        context['is_patient'] = is_patient
        context['is_doctor'] = is_doctor
        return context
