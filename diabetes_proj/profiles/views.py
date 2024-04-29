from typing import Any
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import generic
from login.models import Doctor, Patient
from .models import DoctorsProfileFeedback
from .forms import FeedbackForm, DoctorLinkForm


class DoctorProfile(generic.DetailView):
    model = Doctor
    template_name = 'doctor_profile.html'
    context_object_name = 'doctor'
    paginate_by = 5

    @staticmethod
    def users_role(request):
        user = request.user
        is_patient = user.groups.filter(name='Patients').exists()
        is_doctor = user.groups.filter(name='Doctors').exists()
        return is_patient, is_doctor

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        is_patient, is_doctor = self.users_role(self.request)
        context['is_patient'] = is_patient
        context['is_doctor'] = is_doctor
        context['feedback_form'] = FeedbackForm()
        
        # List of feedbacks about doctor with pagination
        doctor_id = self.object.pk
        feedbacks = DoctorsProfileFeedback.objects.filter(doctor_id=doctor_id)
        paginator = Paginator(feedbacks, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_object = paginator.get_page(page_number)
        context['feedback_list'] = page_object
        return context
    
    def get_object(self, queryset=None):
        if not hasattr(self, 'object'):
            self.object = super().get_object(queryset)
        return self.object
    
    
    @login_required
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        feedback_form = FeedbackForm(request.POST)
        if feedback_form.is_valid():
            feedback = feedback_form.save(commit=False)
            feedback.doctor_id = self.object
            patient = Patient.objects.get(pk = request.user.id)
            feedback.patient_id = patient
            feedback.save()
            return redirect('doctor_profile', pk=self.object.pk)
        return self.render_to_response(self.get_context_data(feedback_form=feedback_form))
    

class PatientProfile(generic.DetailView):
    model = Patient
    template_name = 'patient_profile.html'
    context_object_name = 'patient'

    @staticmethod
    def users_role(request):
        user = request.user
        is_patient = user.groups.filter(name='Patients').exists()
        is_doctor = user.groups.filter(name='Doctors').exists()
        return is_patient, is_doctor
    
    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        is_patient, is_doctor = self.users_role(self.request)
        context['is_patient'] = is_patient
        context['is_doctor'] = is_doctor
        context['link_form'] = DoctorLinkForm()
        return context
    
    def post(self, request, *args, **kwargs):
        patient_id = request.user.id
        link_form = DoctorLinkForm(request.POST)
        if link_form.is_valid():
            token = link_form.cleaned_data['doctor_unique_token']
            doctor = Doctor.objects.get(unique_connect_token = token)
            patient = Patient.objects.get(pk = patient_id)
            patient.doctor_id = doctor
            patient.save()
            return redirect('patient_profile', pk=request.user.id)
        return self.render_to_response(self.get_context_data(link_form = link_form))     


class LinkedPatientList(generic.ListView):
    model = Patient
    template_name = 'patient_list.html'
    context_object_name = 'patient'
    paginate_by = 6
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        patients = Patient.objects.filter(doctor_id = self.request.user.pk)
        context['patients'] = patients
        return context

    
