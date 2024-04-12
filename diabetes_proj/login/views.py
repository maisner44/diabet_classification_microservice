from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import PatientForm
from .models import Patient, Adress

# Create your views here.
class PatientFormView(CreateView):
    model = Patient
    form_class = PatientForm
    template_name = 'login/login.html'
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        # Создаем объект Patient, связываем его с Address и сохраняем все вместе
        patient = form.save(commit=False)
        address = Adress.objects.create(
            country=form.cleaned_data["country"],
            city=form.cleaned_data["city"],
            street=form.cleaned_data["street"],
            house_number=form.cleaned_data["house_number"],
            postal_code=form.cleaned_data["postal_code"]
        )
        patient.adress = address
        patient.save()
        return super().form_valid(form)

