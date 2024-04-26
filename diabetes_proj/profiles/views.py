from typing import Any
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views import generic
from login.models import Doctor, Patient
from .models import DoctorsProfileFeedback
from .forms import FeedbackForm

# Create your views here.
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

    
