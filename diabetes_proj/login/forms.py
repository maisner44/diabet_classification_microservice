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

    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Проверка, существует ли уже пользователь с таким именем
        if Patient.objects.filter(username=username).exists():
            raise forms.ValidationError("Користувач з таким логіном вже існує")
        if (len(username) < 6 ):
            raise forms.ValidationError("Логін занадто короткий")
        return username


class AdressForm(forms.ModelForm):
    class Meta:
        model = Adress
        fields = "__all__"

