from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic, View
from django.urls import reverse, reverse_lazy
from login.models import Patient
from profiles.mixins import UserRoleMixin
from .models import GlucoseMeasurement
from .forms import GlucoseMeasurementForm
from django.core.paginator import Paginator


class GlucoseMeasurmentView(View, UserRoleMixin):
    model = GlucoseMeasurement
    template_name = 'patient_card/glucose.html'
    paginate_by = 84

    def get(self, request, *args, **kwargs):
        """
        Retrieve measurments for current patient grouped by date and paginate by 4 card on page
        """
        glucose_measurements = GlucoseMeasurement.objects.filter(patient_id=self.request.user.id).order_by('-date_of_measurement')

        grouped_dates = {}
        for measurement in glucose_measurements:
            date_key = measurement.date_of_measurement
            if date_key not in grouped_dates:
                grouped_dates[date_key] = []
            grouped_dates[date_key].append(measurement)

        dates_list = list(grouped_dates.items())

        paginator = Paginator(dates_list, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        is_patient, is_doctor = self.get_user_roles(self.request)

        context = {
            'page_obj': page_obj,
            'grouped_dates': grouped_dates,
            'glucose_form': GlucoseMeasurementForm(),
            'is_doctor': is_doctor,
            'is_patient': is_patient,
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