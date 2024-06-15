from django import forms
from django.utils.translation import gettext_lazy as _
from login.models import Doctor, Patient, Adress, Organization
from .models import DoctorsProfileFeedback, TechSupportTicket

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = DoctorsProfileFeedback
        fields = ['feedback_text']
        widgets = {
            'feedback_text': forms.Textarea(attrs={'maxlength': 1000, 'minlength': 20, 'required': True}),
        }


class DoctorLinkForm(forms.Form):
    unique_connect_token = forms.CharField(max_length=255, required=True)


class AdressEditForm(forms.ModelForm):
    class Meta:
        model = Adress
        fields = "__all__"
        labels = {
            'country': _('Країна'),
            'city': _('Місто'),
            'street': _('Вулиця'),
            'house_number': _('Номер будинку'),
            'postal_code': _('Поштовий індекс'),
        }

    def __init__(self, *args, **kwargs):
        super(AdressEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class PatientEditProfileForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = "__all__"
        exclude = ["doctor_id", 
                   "adress_id", 
                   "connect_to_doctor_date", 
                   "body_mass_index",
                   "username",
                   "password",
                   "is_staff",
                   "is_active",
                   "is_superuser",
                   "last_login",
                   "groups",
                   "user_permissions",
                   "date_joined",
                   "id",
                   'age',]
        labels = {
            'phone_number': _('Номер телефону'),
            'date_of_birth': _('Дата народження'),
            'sex': _('Стать'),
            'age': _('Вік'),
            'patronymic': _('По-батькові'),
            'avatar': _('Аватарка'),
            'height': _('Зріст'),
            'weight': _('Вага'),
            'diabet_type': _('Тип діабету'),
            'is_oninsuline': _('Інсулінозалежність'),
        }

    def __init__(self, *args, **kwargs):
        super(PatientEditProfileForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = "__all__"
        exclude = ["adress_id",]
        labels = {
            'organization_name': _('Назва організації'),
            'organization_logo': _('Лого організації'),
            'organization_phone': _('Телефон організації'),
            'organization_email': _('Пошта організації'),
            'organization_description': _('Про організацію'),
            'organization_website_url': _('Сайт організації'),
        }

    def __init__(self, *args, **kwargs):
        super(OrganizationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class DoctorEditProfileForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = "__all__"
        exclude = ["organization_id", 
                   "unique_connect_token",
                   "body_mass_index",
                   "username",
                   "password",
                   "is_staff",
                   "is_active",
                   "is_superuser",
                   "last_login",
                   "groups",
                   "user_permissions",
                   "date_joined",
                   "id",
                   'age',]
        labels = {
            'phone_number': _('Номер телефону'),
            'date_of_birth': _('Дата народження'),
            'sex': _('Стать'),
            'age': _('Вік'),
            'patronymic': _('По-батькові'),
            'avatar': _('Аватарка'),
            'work_experience': _('Стаж роботи'),
            'specialization': _('Спеціалізація'),
            'category': _('Категорія'),
            'about': _('Про себе'),
            'certificate_or_diploma': _('Сертифікат чи диплом'),
        }

    def __init__(self, *args, **kwargs):
        super(DoctorEditProfileForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class TechTicketForm(forms.ModelForm):
    class Meta:
        model = TechSupportTicket
        fields = "__all__"
        exclude = ["user"]
        labels = {
            "text": _('Опишіть вашу проблему'),
            "email": _('Вкажіть електронну пошту'),
            "img": _('Скріншот проблеми(за наявності)'),
        }

    def __init__(self, *args, **kwargs):
        super(TechTicketForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})