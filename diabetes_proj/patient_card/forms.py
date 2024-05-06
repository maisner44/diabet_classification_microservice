from django import forms
from .models import GlucoseMeasurement

class GlucoseMeasurementForm(forms.ModelForm):
    model = GlucoseMeasurement
    fields = "__all__"