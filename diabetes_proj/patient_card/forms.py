from django import forms
from .models import GlucoseMeasurement

class GlucoseMeasurementForm(forms.ModelForm):
    class Meta:
        model = GlucoseMeasurement
        fields = "__all__"
        exclude = ["patient_id",]

    def __init__(self, *args, **kwargs):
        super(GlucoseMeasurementForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            if field_name == 'date_of_measurement':
                field.widget.input_type = 'date'