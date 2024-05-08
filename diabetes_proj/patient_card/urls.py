from django.urls import path
from .views import GlucoseMeasurmentView

urlpatterns = [
    path('<int:patient_id>', GlucoseMeasurmentView.as_view(), name='patient_card'),
]