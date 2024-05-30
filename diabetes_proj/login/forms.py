import re
from django import forms
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Patient, Adress, Doctor
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from PIL import Image

class CustomDiascreenUserValidator:
    def clean_username(form, username):
        if Patient.objects.filter(username=username).exists() or Patient.objects.filter(username=username).exists():
            raise forms.ValidationError("Користувач з таким логіном вже існує")
        if (len(username) < 6 or len(username) > 32):
            raise forms.ValidationError("Логін занадто короткий")
        return username
    
    def clean_password(form, password):
        if (len(password) < 6):
            raise forms.ValidationError("Пароль занадто короткий")
        elif (len(password) > 32):
            raise forms.ValidationError("Пароль занадто довгий")
        return password
        
    def clean_email(form, email):
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError("Некоректна email-адреса")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Користувач з таким email вже існує")
        return email
    
    def clean_date_of_birth(self, date_of_birth):
        if date_of_birth > timezone.now().date():
            raise forms.ValidationError("Дата народження не може бути в майбутньому")
        return date_of_birth
    
    def clean_height(self, height):
        if height <= 0 or height > 300:
            raise forms.ValidationError("Некоректний зріст")
        return height

    def clean_weight(self, weight):
        if weight <= 0 or weight > 500:
            raise forms.ValidationError("Некоректна вага")
        return weight
    
    def clean_nondigits(self, name):
        if not re.match(r'^[a-zA-Zа-яА-ЯёЁіІїЇєЄ]+$', name):
            raise forms.ValidationError("Рядок не може містити цифри або символи")
        return name
    
    def clean_nonletters(self, name):
        if re.match(r'^[a-zA-Zа-яА-ЯёЁіІїЇєЄ]+$', name):
            raise forms.ValidationError("Рядок не може містити цифри або символи")
        return name
    


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
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        return self.validator.clean_password(password)
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        return self.validator.clean_email(email)
    
    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        return self.validator.clean_date_of_birth(date_of_birth)

    def clean_height(self):
        height = self.cleaned_data.get('height')
        return self.validator.clean_height(height)

    def clean_weight(self):
        weight = self.cleaned_data.get('weight')
        return self.validator.clean_weight(weight)
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        return self.validator.clean_nondigits(first_name)
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        return self.validator.clean_nondigits(last_name)
    
    def clean_patronymic(self):
        patronymic = self.cleaned_data.get('patronymic')
        return self.validator.clean_nondigits(patronymic)
    


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
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        return self.validator.clean_password(password)
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        return self.validator.clean_email(email)
    
    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        return self.validator.clean_date_of_birth(date_of_birth)
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        return self.validator.clean_nondigits(first_name)
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        return self.validator.clean_nondigits(last_name)
    
    def clean_patronymic(self):
        patronymic = self.cleaned_data.get('patronymic')
        return self.validator.clean_nondigits(patronymic)
    


class AdressForm(forms.ModelForm):
    class Meta:
        model = Adress
        fields = "__all__"

