from django import forms
from .models import DoctorsProfileFeedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = DoctorsProfileFeedback
        fields = ['feedback_text']
        widgets = {
            'feedback_text': forms.Textarea(attrs={'maxlength': 1000, 'minlength': 20, 'required': True}),
        }


class DoctorLinkForm(forms.Form):
    doctor_unique_token = forms.CharField(max_length=255, required=True)