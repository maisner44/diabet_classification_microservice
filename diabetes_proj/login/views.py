from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login

from .forms import PatientForm, AdressForm, DoctorForm

def registration(request):
    return render(request, 'login/registration.html')

# Create your views here.
def register_patient(request):
    if request.method == "POST":
        patient_form = PatientForm(request.POST)
        address_form = AdressForm(request.POST)
        if patient_form.is_valid() and address_form.is_valid():
            patient = patient_form.save(commit=False)
            address = address_form.save()
            patient.address = address
            patient.save()
            return redirect('home')
        else:
            return render(request, 'login/patient_form.html', {
                'patient_form': patient_form,
                'address_form': address_form,
            })
    else:
        patient_form = PatientForm()
        address_form = AdressForm()
        return render(request, 'login/patient_form.html', {
            'patient_form': patient_form,
            'address_form': address_form,
        })


def register_doctor(request):
    if request.method == "POST":
        doctor_form = DoctorForm(request.POST, request.FILES)
        if doctor_form.is_valid():
            doctor_form.save()
            return redirect('home')
        else:
            return render(request, 'login/doctor_form.html', {'doctor_form': doctor_form})
    else:
        doctor_form = DoctorForm(request.POST)

    return render(request, 'login/doctor_form.html', {'doctor_form': doctor_form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login/login.html', {'form': form})