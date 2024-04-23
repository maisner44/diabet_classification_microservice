from typing import Any
from django.db.models import Q
from django.shortcuts import render
from django.views.generic.list import ListView
from login.models import Doctor
from .forms import DoctorSearchModelForm, DoctorSearchForm

# Create your views here.
class DoctorSearchView(ListView):
    model = Doctor
    paginate_by = 4

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = DoctorSearchModelForm()
        context['search_form'] = DoctorSearchForm()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = DoctorSearchModelForm(self.request.GET)
        search_form = DoctorSearchForm(self.request.GET)

        if search_form.is_valid():
            spivpa = search_form.cleaned_data.get('search_input')
            if spivpa:
                queryset = queryset.filter(
                Q(first_name__icontains=spivpa) | 
                Q(last_name__icontains=spivpa) | 
                Q(patronymic__icontains=spivpa)
            )

        if form.is_valid():
            sex = form.cleaned_data.get('sex')
            category = form.cleaned_data.get('category')
            work_experience = form.cleaned_data.get('work_experience')
            if sex:
                queryset = queryset.filter(sex = sex)
            if category:
                queryset =  queryset.filter(category = category)
            if work_experience:
                queryset = queryset.filter(work_experience__gte = work_experience)
        return queryset
    
  