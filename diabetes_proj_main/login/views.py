from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth import login as auth_login
from django.contrib import messages
from .forms import OTPForm
from django_otp.plugins.otp_email.models import EmailDevice


from .forms import PatientForm, AdressForm, DoctorForm

def registration(request):
    return render(request, 'login/registration.html')


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
        doctor_form = DoctorForm()

    return render(request, 'login/doctor_form.html', {'doctor_form': doctor_form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('handle_otp')
    else:
        form = AuthenticationForm()
    return render(request, 'login/login.html', {'form': form})


@login_required
def handle_otp(request):
    user = request.user
    device, created = EmailDevice.objects.get_or_create(user=user, name='default')

    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            if device.verify_token(otp):
                device.confirmed = True
                device.save()
                messages.success(request, 'Аутентифікація успішна.')
                return redirect('home')
            else:
                messages.error(request, 'Код невірний.')
        else:
            return render(request, 'login/twofactor.html', {'form': form})
    else:
        device.generate_challenge()
        messages.info(request, 'Код відправлено на пошту.')
        form = OTPForm()

    return render(request, 'login/twofactor.html', {'form': form})