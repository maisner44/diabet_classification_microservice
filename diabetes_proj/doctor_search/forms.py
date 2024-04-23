from django import forms



class DoctorSearchForm(forms.Form):
    search_input = forms.CharField(
        max_length=255, 
        required=False, 
        label='Пошук', 
        widget=forms.TextInput(attrs={'placeholder': 'Введіть ім`я, прізвище або по-батькові лікаря'}))


class DoctorSearchModelForm(forms.Form):
    SEX_CHOICES = [
        ('Male', 'Чоловічий'),
        ('Female', 'Жіночий'),
    ]

    CATEGORY_CHOICES = [
        ('Вища категорія', 'Вища категорія'),
        ('Перша категорія', 'Перша категорія'),
        ('Друга категорія', 'Друга категорія'),
    ]

    sex = forms.ChoiceField(choices=SEX_CHOICES, required=False, label='Стать лікаря', widget=forms.RadioSelect)
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, required=False, label='Категорія', widget=forms.RadioSelect)
    work_experience = forms.CharField(required=False, label='Стаж роботи (Мінімальний)', widget=forms.NumberInput)