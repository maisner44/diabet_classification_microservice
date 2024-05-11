from django import forms
from .models import Patient, Adress, Doctor

class CustomDiascreenUserValidator:
    def clean_username(form, username):
        if Patient.objects.filter(username=username).exists() or Patient.objects.filter(username=username).exists():
            raise forms.ValidationError("Користувач з таким логіном вже існує")
        if (len(username) < 6 or len(username) > 32):
            raise forms.ValidationError("Логін занадто короткий")
        return username

class PatientForm(forms.ModelForm):
    validator = CustomDiascreenUserValidator()

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
            "avatar"
        ]

    def clean_username(self):
        username = self.cleaned_data.get('username')
        return self.validator.clean_username(username)


class DoctorForm(forms.ModelForm):
    validator = CustomDiascreenUserValidator()

    class Meta:
        model = Doctor
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
            "work_experience",
            "specialization",
            "category",
            "certificate_or_diploma",
            "about",
            "avatar"
        ]

    def clean_username(self):
        username = self.cleaned_data.get('username')
        return self.validator.clean_username(username)
    


class AdressForm(forms.ModelForm):
    class Meta:
        model = Adress
        fields = "__all__"

