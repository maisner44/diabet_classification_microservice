from typing import Any
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from django.db.models.query import QuerySet
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from login.models import Doctor, Patient, Adress, Organization
from login.forms import PatientForm, AdressForm
from .models import DoctorsProfileFeedback
from .forms import FeedbackForm, DoctorLinkForm, AdressEditForm, PatientEditProfileForm, OrganizationForm, DoctorEditProfileForm
from .mixins import UserRoleMixin


class DoctorProfile(generic.DetailView, UserRoleMixin):
    model = Doctor
    template_name = 'doctor_profile.html'
    context_object_name = 'doctor'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        is_patient, is_doctor = self.get_user_roles(self.request)
        context['is_patient'] = is_patient
        context['is_doctor'] = is_doctor
        context['feedback_form'] = FeedbackForm()
        
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
    

    
class PatientProfile(generic.DetailView, UserRoleMixin):
    model = Patient
    template_name = 'patient_profile.html'
    context_object_name = 'patient'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        is_patient, is_doctor = self.get_user_roles(self.request)
        context['is_patient'] = is_patient
        context['is_doctor'] = is_doctor
        context['link_form'] = DoctorLinkForm()
        return context
    
    def post(self, request, *args, **kwargs):
        link_form = DoctorLinkForm(request.POST)
        if link_form.is_valid():
            token = link_form.cleaned_data['unique_connect_token']
            doctor = get_object_or_404(Doctor, unique_connect_token=token)
            patient = self.get_object()
            patient.doctor_id = doctor
            patient.save(update_fields=['doctor_id', 'connect_to_doctor_date'])
            return redirect('patient_profile', pk=patient.id)
        return render(request, 'patient_profile.html', {'link_form': link_form})

    def get_object(self, queryset=None):
        if not hasattr(self, 'object'):
            self.object = super().get_object(queryset)
        return self.object
    

class DoctorsPatientList(generic.ListView, UserRoleMixin):
    model = Patient
    paginate_by = 3
    template_name = 'doctor_patients_list.html'
    context_object_name = 'patient_list'
    
    def get_queryset(self):
        doctor = self.request.user
        queryset = Patient.objects.filter(doctor_id = doctor)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        is_patient, is_doctor = self.get_user_roles(self.request)
        context['is_patient'] = is_patient
        context['is_doctor'] = is_doctor
        return context
    

def edit_patient_profile(request, patient_id):
    
    if (patient_id == request.user.id):
        patient = get_object_or_404(Patient, id=patient_id)
        address = patient.adress_id
    else:
        return HttpResponseForbidden('У вас немає відповідного доступу')

    if request.method == 'POST':
        patient_form = PatientEditProfileForm(request.POST, instance=patient)
        address_form = AdressEditForm(request.POST, instance=address)
        
        if patient_form.is_valid() and address_form.is_valid():
            patient = patient_form.save(commit=False)
            address = address_form.save()
            patient.adress_id = address
            patient.save()
            return redirect('patient_profile', pk=patient.id)
    else:
        patient_form = PatientEditProfileForm(instance=patient)
        address_form = AdressEditForm(instance=address)
    
    return render(request, 'profiles/edit_patient_profile.html', {
        'patient_form': patient_form,
        'address_form': address_form,
        'patient': patient
    })


def edit_doctor_profile(request, doctor_id):
    
    doctor = get_object_or_404(Doctor, id=doctor_id)

    if doctor_id != request.user.id:
        return HttpResponseForbidden('У вас немає відповідного доступу')
    organization = doctor.organization_id
    if organization is None:
        organization = Organization()  
        address = Adress()
    else:
        address = organization.adress_id

    if request.method == 'POST':
        doctor_form = DoctorEditProfileForm(request.POST, request.FILES, instance=doctor)
        org_form = OrganizationForm(request.POST, request.FILES, instance=organization)
        address_form = AdressEditForm(request.POST, instance=address)
        
        if doctor_form.is_valid() and address_form.is_valid() and org_form.is_valid():
            doctor = doctor_form.save(commit=False)
            org = org_form.save(commit=False)
            address = address_form.save()
            org.adress_id = address
            org.save()
            doctor.organization_id = org
            doctor.save()
            return redirect('doctor_profile', pk=doctor.id)
    else:
        doctor_form = DoctorEditProfileForm(instance=doctor)
        org_form = OrganizationForm(instance=organization)
        address_form = AdressEditForm(instance=address)
    
    return render(request, 'profiles/edit_doctor_profile.html', {
        'doctor_form': doctor_form,
        'org_form': org_form,
        'address_form': address_form,
        'doctor': doctor
    })