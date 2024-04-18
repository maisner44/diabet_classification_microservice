from django.shortcuts import render
from django.views import generic
from login.models import Doctor

# Create your views here.
class DoctorSearchView(generic.ListView):
    class Meta:
        model = Doctor
