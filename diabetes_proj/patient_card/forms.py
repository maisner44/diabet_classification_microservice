from django import forms
from django.utils.translation import gettext_lazy as _
from .models import GlucoseMeasurement, PhysicalActivityMeasurement, TypeOfActivity, FoodMeasurement, FoodItem, InsulineDoseMeasurement

class GlucoseMeasurementForm(forms.ModelForm):
    class Meta:
        model = GlucoseMeasurement
        fields = "__all__"
        exclude = ["patient_id",]
        labels = {
            'glucose': _('Кількість глюкози в крові (ммоль/л)'),
            'glucose_measurement_category': _('Категорія'),
            'date_of_measurement': _('Дата заміру'),
            'time_of_measurement': _('Час заміру'),
        }

    def __init__(self, *args, **kwargs):
        super(GlucoseMeasurementForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            if field_name == 'date_of_measurement':
                field.widget.input_type = 'date'


class PhysicalActivityForm(forms.ModelForm):

    type_of_activity = forms.ModelChoiceField(
        queryset=TypeOfActivity.objects.all(),
        label='Тип активності',
        required=True,
    )

    class Meta:
        model = PhysicalActivityMeasurement
        fields = "__all__"
        exclude = ["patient_id",]
        labels = {
            'number_of_approaches': _('Кількість підходів'),
            'commentary': _('Короткий коментар (що конкретно робили)'),
            'date_of_measurement': _('Дата заміру'),
            'time_of_activity': _('Час заміру'),
        }

    def __init__(self, *args, **kwargs):
        super(PhysicalActivityForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            if field_name == 'date_of_measurement':
                field.widget.input_type = 'date'


class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = "__all__"
        labels = {
            'name': _('Назва страви'),
            'proteins': _('Кількість білків'),
            'fats': _('Кількість жирів'),
            'carbohydrates': _('Кількість вуглеводів'),
        }
        

    def __init__(self, *args, **kwargs):
        super(FoodItemForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class FoodMeasurementForm(forms.ModelForm):
    class Meta:
        model = FoodMeasurement
        fields = "__all__"
        exclude = ["patient_id","food_items","bread_unit", "insuline_dose_after"]
        labels = {
            'insuline_dose_before': _('Доза інсуліну до їжі'),
            'date_of_measurement': _('Дата прийому їжі'),
            'time_of_activity': _('Час прийому їжі'),
        }

    def __init__(self, *args, **kwargs):
        super(FoodMeasurementForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            if field_name == 'date_of_measurement':
                field.widget.input_type = 'date'


class InsulineDoseForm(forms.ModelForm):
    class Meta:
        model = InsulineDoseMeasurement
        fields = "__all__"
        exclude = ["patient_id",]
        labels = {
            'category': _('Категорія'),
            'insuline_dose': _('Доза інсуліну (ОД)'),
            'date_of_measurement': _('Дата заміру'),
            'time': _('Час заміру'),
        }

    def __init__(self, *args, **kwargs):
        super(InsulineDoseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            if field_name == 'date_of_measurement':
                field.widget.input_type = 'date'