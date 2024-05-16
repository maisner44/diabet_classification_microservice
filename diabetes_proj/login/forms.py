from django import forms
from .models import Patient, Adress, Doctor
from django.utils.translation import gettext_lazy as _

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
        labels = {
            "username": _('Логін'),
            "email": _('Електронна пошта'),
            "password": _('Пароль'),
            "phone_number": _('Номер телефону'),
            "date_of_birth": _('Дата народження'),
            "sex": _('Стать'),
            "first_name": _('Ім`я'),
            "last_name": _('Прізвище'),
            "patronymic": _('По-батькові'),
            "height": _('Зріст'),
            "weight": _('Вага'),
            "diabet_type": _('Тип діабету'),
            "avatar": _('Аватар профілю'),
        }

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
        labels = {
            "username": _('Логін'),
            "email": _('Електронна пошта'),
            "password": _('Пароль'),
            "phone_number": _('Номер телефону'),
            "date_of_birth": _('Дата народження'),
            "sex": _('Стать'),
            "first_name": _('Ім`я'),
            "last_name": _('Прізвище'),
            "patronymic": _('По-батькові'),
            "work_experience": _('Стаж роботи'),
            "specialization": _('Спеціальность'),
            "category": _('Категорія лікаря'),
            "certificate_or_diploma": _('Сертифікат або диплом'),
            "about": _('Про себе'),
            "avatar": _('Аватар профілю'),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        return self.validator.clean_username(username)
    


class AdressForm(forms.ModelForm):
    class Meta:
        model = Adress
        fields = "__all__"

