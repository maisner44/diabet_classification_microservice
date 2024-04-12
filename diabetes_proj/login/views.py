from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login

from .forms import PatientForm, AdressForm

# Create your views here.
def register_patient(request):
    if request.method == "POST":
        patient_form = PatientForm(request.POST)
        adress_form = AdressForm(request.POST)
        if patient_form.is_valid() and adress_form.is_valid():
            patient = patient_form.save(commit=False)
            adress = adress_form.save()
            patient.adress = adress
            patient.save()

            return redirect('home')
        else:
            return render(request, 'login/registration.html', {'patient_form': patient_form, 'address_form': adress_form})
    else:
        patient_form = PatientForm()
        adress_form = AdressForm()
        return render(request, 'login/registration.html', {'patient_form': patient_form, 'address_form': adress_form})
    

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login/login.html', {'form': form})