from django import forms
from .models import Patient, Adress

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            "username",
            "email",
            "password",
            "phone_number",
            "date_of_birth",
            "sex",
            "first_name",
            "last_name",
            "patronymic",
            "height",
            "weight",
            "diabet_type",
        ]
        


class AdressForm(forms.ModelForm):
    class Meta:
        model = Adress
        fields = "__all__"

