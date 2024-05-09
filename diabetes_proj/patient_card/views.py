
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic, View
from django.urls import reverse, reverse_lazy
from login.models import Patient
from profiles.mixins import UserRoleMixin
from .models import GlucoseMeasurement, PhysicalActivityMeasurement
from .forms import GlucoseMeasurementForm, PhysicalActivityForm
from .utils.utils import groupe_by_date


class GlucoseMeasurmentView(View, UserRoleMixin):
    model = GlucoseMeasurement
    template_name = 'patient_card/glucose.html'
    paginate_by = 24

    def get(self, request, patient_id, *args, **kwargs):
        """
        Retrieve measurments for current patient grouped by date and paginate by 4 card on page
        """
        is_patient, is_doctor = self.get_user_roles(self.request)
        if (is_doctor):
            glucose_measurements = GlucoseMeasurement.objects.filter(patient_id=patient_id).order_by('-date_of_measurement')
        elif (self.request.user.id != patient_id):
            return HttpResponseForbidden('У вас немає доступу до цього ресурсу')
        else:
            glucose_measurements = GlucoseMeasurement.objects.filter(patient_id=self.request.user.id).order_by('-date_of_measurement')

        
        grouped_dates, dates_list = groupe_by_date(glucose_measurements)
        paginator = Paginator(dates_list, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)


        context = {
            'page_obj': page_obj,
            'grouped_dates': grouped_dates,
            'glucose_form': GlucoseMeasurementForm(),
            'is_doctor': is_doctor,
            'is_patient': is_patient,
            'patient_id': patient_id,
        }
        return render(request, self.template_name, context)
    

    def post(self, request, patient_id, *args, **kwargs):
        form = GlucoseMeasurementForm(request.POST)
        if form.is_valid():
            patient = get_object_or_404(Patient, id=request.user.id)
            glucose_measurement = form.save(commit=False)
            glucose_measurement.patient_id = patient
            glucose_measurement.save()          
            redirect_url = reverse_lazy('patient_card', kwargs={'patient_id': patient_id})
            return redirect(redirect_url)
        else:
            return render(request, self.template_name, {'form': form})
        

class PhysicalMeasurementView(View, UserRoleMixin):
    model = PhysicalActivityMeasurement
    template_name = 'patient_card/physical.html'
    paginate_by = 24

    def get(self, request, patient_id, *args, **kwargs):
        """
        Retrieve measurments for current patient grouped by date and paginate it
        """
        is_patient, is_doctor = self.get_user_roles(self.request)
        if (is_doctor):
            fit_measurements = PhysicalActivityMeasurement.objects.filter(patient_id=patient_id).order_by('-date_of_measurement')
        elif (self.request.user.id != patient_id):
            return HttpResponseForbidden('У вас немає доступу до цього ресурсу')
        else:
            fit_measurements = PhysicalActivityMeasurement.objects.filter(patient_id=self.request.user.id).order_by('-date_of_measurement')
       

        grouped_dates, dates_list = groupe_by_date(fit_measurements)
        paginator = Paginator(dates_list, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'page_obj': page_obj,
            'grouped_dates': grouped_dates,
            'activity_form': PhysicalActivityForm(),
            'is_doctor': is_doctor,
            'is_patient': is_patient,
            'patient_id': patient_id,
        }
        return render(request, self.template_name, context)
    

    def post(self, request, patient_id, *args, **kwargs):
        form = PhysicalActivityForm(request.POST)
        if form.is_valid():
            patient = get_object_or_404(Patient, id=request.user.id)
            physical_activity = form.save(commit=False)
            physical_activity.patient_id = patient
            physical_activity.save()
            
            redirect_url = reverse_lazy('patient_physics', kwargs={'patient_id': patient_id})
            return redirect(redirect_url)
        else:
            return render(request, self.template_name, {'form': form})
        

