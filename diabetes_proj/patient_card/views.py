
from django.core.paginator import Paginator
from django.forms import modelformset_factory
from django.http import HttpResponseForbidden, FileResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic, View
from django.urls import reverse, reverse_lazy
from login.models import Patient
from profiles.mixins import UserRoleMixin
from .models import GlucoseMeasurement, PhysicalActivityMeasurement, FoodMeasurement, FoodItem, InsulineDoseMeasurement, Analysis, AnalysType
from .forms import GlucoseMeasurementForm, PhysicalActivityForm, FoodMeasurementForm, FoodItemForm, InsulineDoseForm, AnalysisForm, AnalysisTypeForm
from .utils.utils import group_by_date


class GlucoseMeasurmentView(View, UserRoleMixin):
    model = GlucoseMeasurement
    template_name = 'patient_card/glucose.html'
    paginate_by = 24

    def get_context_data(self, patient_id, **kwargs):
        
        is_patient, is_doctor = self.get_user_roles(self.request)
        
        if is_doctor:
            glucose_measurements = GlucoseMeasurement.objects.filter(patient_id=patient_id).order_by('-date_of_measurement')
        elif self.request.user.id != patient_id:
            raise HttpResponseForbidden('У вас немає доступу до цього ресурсу')
        else:
            glucose_measurements = GlucoseMeasurement.objects.filter(patient_id=self.request.user.id).order_by('-date_of_measurement')

        grouped_dates, dates_list = group_by_date(glucose_measurements)
        paginator = Paginator(dates_list, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        patient = get_object_or_404(Patient, id=patient_id)

        context = {
            'page_obj': page_obj,
            'grouped_dates': grouped_dates,
            'glucose_form': GlucoseMeasurementForm(),
            'is_doctor': is_doctor,
            'is_patient': is_patient,
            'patient_id': patient_id,
            'is_oninsuline': patient.is_oninsuline,
        }
        return context


    def get(self, request, patient_id, *args, **kwargs):
        """
        Retrieve measurments for current patient grouped by date and paginate by 4 card on page
        """
        context = self.get_context_data(patient_id)
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
            context = self.get_context_data(patient_id)
            return render(request, self.template_name, context)
            
        
class PhysicalMeasurementView(View, UserRoleMixin):
    model = PhysicalActivityMeasurement
    template_name = 'patient_card/physical.html'
    paginate_by = 24

    def get_context_data(self, patient_id, **kwargs):
        is_patient, is_doctor = self.get_user_roles(self.request)
        if (is_doctor):
            fit_measurements = PhysicalActivityMeasurement.objects.filter(patient_id=patient_id).order_by('-date_of_measurement')
        elif (self.request.user.id != patient_id):
            return HttpResponseForbidden('У вас немає доступу до цього ресурсу')
        else:
            fit_measurements = PhysicalActivityMeasurement.objects.filter(patient_id=self.request.user.id).order_by('-date_of_measurement')
       

        grouped_dates, dates_list = group_by_date(fit_measurements)
        paginator = Paginator(dates_list, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        patient = get_object_or_404(Patient, id=patient_id)

        context = {
            'page_obj': page_obj,
            'grouped_dates': grouped_dates,
            'activity_form': PhysicalActivityForm(),
            'is_doctor': is_doctor,
            'is_patient': is_patient,
            'patient_id': patient_id,
            'is_oninsuline': patient.is_oninsuline,
        }
        return context


    def get(self, request, patient_id, *args, **kwargs):
        """
        Retrieve measurments for current patient grouped by date and paginate by 4 card on page
        """
        context = self.get_context_data(patient_id)
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
            context = self.get_context_data(patient_id)
            return render(request, self.template_name, context)
        

class FoodMeasurementView(View, UserRoleMixin):
    model = FoodMeasurement
    template_name = 'patient_card/food.html'
    initial_food_item_count = 1
    paginate_by = 24

    def get_context_data(self, patient_id, **kwargs):
        is_patient, is_doctor = self.get_user_roles(self.request)
        
        if is_doctor:
            food_measurements = FoodMeasurement.objects.filter(patient_id=patient_id).order_by('-date_of_measurement')
        elif self.request.user.id != patient_id:
            return HttpResponseForbidden('У вас нет доступа к этому ресурсу')
        else:
            food_measurements = FoodMeasurement.objects.filter(patient_id=self.request.user.id).order_by('-date_of_measurement')

        grouped_dates, dates_list = group_by_date(food_measurements)
        paginator = Paginator(dates_list, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        patient = get_object_or_404(Patient, id=patient_id)

        context = {
            'page_obj': page_obj,
            'grouped_dates': grouped_dates,
            'food_measurement': FoodMeasurementForm(),
            'food_item_forms': [FoodItemForm(prefix=f'food_item_{i}') for i in range(self.initial_food_item_count)],
            'is_doctor': is_doctor,
            'is_patient': is_patient,
            'patient_id': patient_id,
            'is_oninsuline': patient.is_oninsuline,
        }
        return context

    def get(self, request, patient_id, *args, **kwargs):
        context = self.get_context_data(patient_id)
        return render(request, self.template_name, context)

    def post(self, request, patient_id, *args, **kwargs):
        measurement_form = FoodMeasurementForm(request.POST)
        
        if measurement_form.is_valid():
            patient = get_object_or_404(Patient, id=request.user.id)
            measurement = measurement_form.save(commit=False)
            measurement.patient_id = patient
            measurement.save()

            prefixes = set(key.split('-')[0] for key in request.POST if key.startswith('food_item_'))
            for prefix in prefixes:
                form = FoodItemForm(request.POST, prefix=prefix)
                if form.is_valid():
                    print(form.cleaned_data)
                    food_item = FoodItem(
                        name=form.cleaned_data['name'],
                        proteins=form.cleaned_data['proteins'],
                        fats=form.cleaned_data['fats'],
                        carbohydrates=form.cleaned_data['carbohydrates']
                    )      
                    food_item.save()
                    measurement.food_items.add(food_item)
                else:
                    print(f"Form {prefix} errors: {form.errors}")

            measurement.bread_unit = measurement.calculate_bread_unit()
            measurement.save()
            redirect_url = reverse_lazy('patient_food', kwargs={'patient_id': patient_id})
            return redirect(redirect_url)
        else:
            context = self.get_context_data(patient_id)
            return render(request, self.template_name, context)
        

class InsulineDoseView(View, UserRoleMixin):
    model = InsulineDoseMeasurement
    template_name = 'patient_card/insuline.html'
    paginate_by = 24

    def get_context_data(self, patient_id, **kwargs):
        is_patient, is_doctor = self.get_user_roles(self.request)
        if (is_doctor):
            insuline_measurements = InsulineDoseMeasurement.objects.filter(patient_id=patient_id).order_by('-date_of_measurement')
        elif (self.request.user.id != patient_id):
            return HttpResponseForbidden('У вас немає доступу до цього ресурсу')
        else:
            insuline_measurements = InsulineDoseMeasurement.objects.filter(patient_id=self.request.user.id).order_by('-date_of_measurement')
       
        
        grouped_dates, dates_list = group_by_date(insuline_measurements)
        paginator = Paginator(dates_list, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        patient = get_object_or_404(Patient, id=patient_id)

        context = {
            'page_obj': page_obj,
            'grouped_dates': grouped_dates,
            'insuline_form': InsulineDoseForm(),
            'is_doctor': is_doctor,
            'is_patient': is_patient,
            'patient_id': patient_id,
            'is_oninsuline': patient.is_oninsuline,
        }
        return context


    def get(self, request, patient_id, *args, **kwargs):
        """
        Retrieve measurments for current patient grouped by date and paginate by 4 card on page
        """
        context = self.get_context_data(patient_id)
        return render(request, self.template_name, context)
    

    def post(self, request, patient_id, *args, **kwargs):
        form = InsulineDoseForm(request.POST)
        if form.is_valid():
            patient = get_object_or_404(Patient, id=request.user.id)
            insuline = form.save(commit=False)
            insuline.patient_id = patient
            insuline.save()
            
            redirect_url = reverse_lazy('patient_insuline', kwargs={'patient_id': patient_id})
            return redirect(redirect_url)
        else:
            context = self.get_context_data(patient_id)
            return render(request, self.template_name, context)
        

class AnalysisLoadView(View, UserRoleMixin):
    model = Analysis
    template_name = 'patient_card/analysis.html'
    paginate_by = 8

    def get_context_data(self, patient_id, **kwargs):
        
        is_patient, is_doctor = self.get_user_roles(self.request)
        
        if is_doctor:
            analysis = Analysis.objects.filter(patient_id=patient_id).order_by('-date_of_measurement')
        elif self.request.user.id != patient_id:
            raise HttpResponseForbidden('У вас немає доступу до цього ресурсу')
        else:
            analysis = Analysis.objects.filter(patient_id=self.request.user.id).order_by('-date_of_measurement')

        paginator = Paginator(analysis, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'page_obj': page_obj,
            'type_form': AnalysisTypeForm(),
            'analysis_form': AnalysisForm(),
            'is_doctor': is_doctor,
            'is_patient': is_patient,
            'patient_id': patient_id,
        }
        return context


    def get(self, request, patient_id, *args, **kwargs):
        """
        Retrieve measurments for current patient grouped by date and paginate by 4 card on page
        """
        context = self.get_context_data(patient_id)
        return render(request, self.template_name, context)
    

    def post(self, request, patient_id, *args, **kwargs):
        analysis_form = AnalysisForm(request.POST, request.FILES)
        analysis_type_form = AnalysisTypeForm(request.POST)
        if analysis_form.is_valid() and analysis_type_form.is_valid():
            patient = get_object_or_404(Patient, id=request.user.id)
            analysis = analysis_form.save(commit=False)

            _type = analysis_type_form.cleaned_data['name']
            if (AnalysType.objects.filter(name = _type).exists()):
                analysis_type = get_object_or_404(AnalysType, name=_type)
            else:
                analysis_type = analysis_type_form.save()

            analysis.analysis_type = analysis_type
            analysis.patient_id = patient
            analysis.save()          
            redirect_url = reverse_lazy('patient_analysis', kwargs={'patient_id': patient_id})
            return redirect(redirect_url)
        else:
            context = self.get_context_data(patient_id)
            return render(request, self.template_name, context)

from django.conf import settings
import os

def download_pdf(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    analysis = get_object_or_404(Analysis, patient_id=patient)
    file_url = analysis.get_file_url()
    file_path = os.path.join(settings.MEDIA_ROOT, file_url.lstrip('/'))
    print(file_url)
    response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}.pdf"'
    return response