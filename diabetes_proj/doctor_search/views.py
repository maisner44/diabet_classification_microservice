from django.shortcuts import render
from django.views.generic.list import ListView
from login.models import Doctor

# Create your views here.
class DoctorSearchView(ListView):
    model = Doctor
    paginate_by = 4
    
  